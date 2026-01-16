"""Router for Tournament endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from sqlalchemy import text
from typing import List, Optional
import logging
import traceback
from app import schemas
from app.database import get_db
from app.crud import tournaments, seasons, players, decks, matches as matches_crud

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tournaments", tags=["Tournaments"])


@router.get("/", response_model=List[schemas.Tournament])
def list_tournaments(
    skip: int = 0,
    limit: int = 100,
    season_id: Optional[int] = Query(None, description="Filter by season ID"),
    db: Session = Depends(get_db)
):
    """
    Get list of all tournaments.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **season_id**: Optional filter by season
    """
    return tournaments.get_tournaments(db, skip=skip, limit=limit, season_id=season_id)


@router.get("/{tournament_id}", response_model=schemas.Tournament)
def get_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Get a specific tournament by ID."""
    db_tournament = tournaments.get_tournament(db, tournament_id=tournament_id)
    if not db_tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament with id {tournament_id} not found"
        )
    return db_tournament


@router.post("/", response_model=schemas.Tournament, status_code=status.HTTP_201_CREATED)
def create_tournament(tournament: schemas.TournamentCreate, db: Session = Depends(get_db)):
    """
    Create a new tournament.
    
    - **season_id**: Season ID (required)
    - **name**: Tournament name (required)
    - **tournament_date**: Tournament date (required)
    - **location**: Tournament location (optional)
    - **format**: MTG format like Standard, Modern (optional)
    - **description**: Tournament description (optional)
    """
    try:
        return tournaments.create_tournament(db=db, tournament=tournament)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/{tournament_id}", response_model=schemas.Tournament)
def update_tournament(
    tournament_id: int,
    tournament: schemas.TournamentUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing tournament."""
    try:
        db_tournament = tournaments.update_tournament(db, tournament_id=tournament_id, tournament=tournament)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not db_tournament:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament with id {tournament_id} not found"
        )
    return db_tournament


@router.delete("/{tournament_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tournament(tournament_id: int, db: Session = Depends(get_db)):
    """Delete a tournament (and all its matches)."""
    if not tournaments.delete_tournament(db, tournament_id=tournament_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament with id {tournament_id} not found"
        )
    return None


@router.post("/import-complete", response_model=schemas.TournamentImportResponse, status_code=status.HTTP_201_CREATED)
def import_complete_tournament(
    data: schemas.TournamentCompleteImport,
    db: Session = Depends(get_db)
):
    """
    Import complete tournament data in a single request.
    
    This endpoint creates/updates all necessary entities:
    - Tournament (creates new tournament)
    - Players (creates if they don't exist, looks up by name)
    - Deck Archetypes (creates if they don't exist, looks up by name)
    - Matches and Games (creates all match results)
    
    **Example JSON:**
    ```json
    {
      "season_id": 1,
      "tournament": {
        "name": "January FNM",
        "tournament_date": "2026-01-20",
        "location": "Local Game Store",
        "format": "Standard"
      },
      "players": [
        {"name": "Alice Johnson", "email": "alice@email.com"},
        {"name": "Bob Smith", "email": "bob@email.com"}
      ],
      "decks": [
        {"name": "Mono Red Aggro", "color_identity": "R", "archetype_type": "Aggro"},
        {"name": "Azorius Control", "color_identity": "WU", "archetype_type": "Control"}
      ],
      "matches": [
        {
          "round_number": 1,
          "player1_name": "Alice Johnson",
          "player2_name": "Bob Smith",
          "player1_deck_name": "Mono Red Aggro",
          "player2_deck_name": "Azorius Control",
          "games": [
            {"game_number": 1, "winner_name": "Alice Johnson", "duration_minutes": 12},
            {"game_number": 2, "winner_name": "Bob Smith", "duration_minutes": 18},
            {"game_number": 3, "winner_name": "Alice Johnson", "duration_minutes": 15}
          ]
        }
      ]
    }
    ```
    """
    from app.crud import players, decks, matches as matches_crud
    from app import models
    from sqlalchemy import text
    
    try:
        logger.info(f"Starting tournament import for season {data.season_id}")
        logger.info(f"Tournament: {data.tournament.name}, Players: {len(data.players)}, Decks: {len(data.decks)}, Matches: {len(data.matches)}")
        
        # Verify season exists
        logger.info(f"Verifying season {data.season_id} exists...")
        season_query = db.execute(
            text("SELECT id, name FROM seasons WHERE id = :season_id"),
            {"season_id": data.season_id}
        ).fetchone()
        
        if not season_query:
            logger.error(f"Season {data.season_id} not found")
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Season with id {data.season_id} not found"
            )
        logger.info(f"Season verified: {season_query[1]}")
        
        # Create tournament
        logger.info(f"Creating tournament: {data.tournament.name}")
        tournament_create = schemas.TournamentCreate(
            season_id=data.season_id,
            name=data.tournament.name,
            tournament_date=data.tournament.tournament_date,
            location=data.tournament.location,
            format=data.tournament.format,
            description=data.tournament.description,
            tournament_type_id=data.tournament.tournament_type_id,
            tournament_type_name=data.tournament.tournament_type_name,
        )
        try:
            new_tournament = tournaments.create_tournament(db, tournament_create)
        except ValueError as exc:
            logger.error(f"Tournament type resolution failed: {exc}")
            raise HTTPException(
                status_code=status.HTTP_400_BAD_REQUEST,
                detail=str(exc)
            )
        logger.info(f"Tournament created with ID: {new_tournament.id}")
        
        # Track created entities
        created_players = 0
        created_decks = 0
        created_matches = 0
        created_games = 0
        
        # Create player name -> ID mapping
        player_map = {}
        
        # Process players: create if don't exist, build mapping
        logger.info("Processing players...")
        all_player_names = set()
        for player_import in data.players:
            all_player_names.add(player_import.name)
        for match in data.matches:
            all_player_names.add(match.player1_name)
            all_player_names.add(match.player2_name)
            for game in match.games:
                all_player_names.add(game.winner_name)
        
        logger.info(f"Found {len(all_player_names)} unique players to process")
        
        for player_name in all_player_names:
            # Check if player exists
            logger.debug(f"Processing player: {player_name}")
            existing = players.get_player_by_name(db, player_name)
            if existing:
                logger.debug(f"Player '{player_name}' exists with ID {existing.id}")
                player_map[player_name] = existing.id
            else:
                # Find player data from import list
                player_data = next((p for p in data.players if p.name == player_name), None)
                player_create = schemas.PlayerCreate(
                    name=player_name,
                    email=player_data.email if player_data else None,
                    active=True
                )
                new_player = players.create_player(db, player_create)
                logger.info(f"Created new player '{player_name}' with ID {new_player.id}")
                player_map[player_name] = new_player.id
                created_players += 1
        
        logger.info(f"Players processed: {created_players} created, {len(all_player_names) - created_players} existing")
        
        # Create deck name -> ID mapping
        deck_map = {}
        
        # Process decks: create if don't exist, build mapping
        logger.info("Processing decks...")
        all_deck_names = set()
        for deck_import in data.decks:
            all_deck_names.add(deck_import.name)
        for match in data.matches:
            all_deck_names.add(match.player1_deck_name)
            all_deck_names.add(match.player2_deck_name)
        
        logger.info(f"Found {len(all_deck_names)} unique decks to process")
        
        for deck_name in all_deck_names:
            # Check if deck exists
            logger.debug(f"Processing deck: {deck_name}")
            existing = decks.get_deck_by_name(db, deck_name)
            if existing:
                logger.debug(f"Deck '{deck_name}' exists with ID {existing.id}")
                deck_map[deck_name] = existing.id
            else:
                # Find deck data from import list
                deck_data = next((d for d in data.decks if d.name == deck_name), None)
                if not deck_data:
                    logger.error(f"Deck '{deck_name}' used in matches but not defined in decks array")
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=f"Deck '{deck_name}' referenced in matches but not defined in decks array"
                    )
                deck_create = schemas.DeckArchetypeCreate(
                    name=deck_name,
                    color_identity=deck_data.color_identity if deck_data else "C",
                    archetype_type=deck_data.archetype_type if deck_data else "Other",
                    description=deck_data.description if deck_data else None
                )
                new_deck = decks.create_deck_archetype(db, deck_create)
                logger.info(f"Created new deck '{deck_name}' with ID {new_deck.id}")
                deck_map[deck_name] = new_deck.id
                created_decks += 1
        
        logger.info(f"Decks processed: {created_decks} created, {len(all_deck_names) - created_decks} existing")
        
        # Process matches and games
        logger.info(f"Processing {len(data.matches)} matches...")
        for idx, match_import in enumerate(data.matches, 1):
            logger.info(f"Processing match {idx}/{len(data.matches)}: Round {match_import.round_number} - {match_import.player1_name} vs {match_import.player2_name}")
            
            # Resolve IDs
            player1_id = player_map.get(match_import.player1_name)
            player2_id = player_map.get(match_import.player2_name)
            deck1_id = deck_map.get(match_import.player1_deck_name)
            deck2_id = deck_map.get(match_import.player2_deck_name)
            
            if not all([player1_id, player2_id, deck1_id, deck2_id]):
                missing = []
                if not player1_id: missing.append(f"player1 '{match_import.player1_name}'")
                if not player2_id: missing.append(f"player2 '{match_import.player2_name}'")
                if not deck1_id: missing.append(f"deck1 '{match_import.player1_deck_name}'")
                if not deck2_id: missing.append(f"deck2 '{match_import.player2_deck_name}'")
                error_msg = f"Failed to resolve IDs for match {idx}: Missing {', '.join(missing)}"
                logger.error(error_msg)
                raise HTTPException(
                    status_code=status.HTTP_400_BAD_REQUEST,
                    detail=error_msg
                )
            
            logger.debug(f"Match IDs resolved: P1={player1_id}, P2={player2_id}, D1={deck1_id}, D2={deck2_id}")
            
            # Create match
            match_create = schemas.MatchCreate(
                tournament_id=new_tournament.id,
                player1_id=player1_id,
                player2_id=player2_id,
                player1_deck_id=deck1_id,
                player2_deck_id=deck2_id,
                round_number=match_import.round_number,
                match_status="COMPLETED"
            )
            new_match = matches_crud.create_match(db, match_create)
            logger.info(f"Match {idx} created with ID {new_match.id}")
            created_matches += 1
            
            # Create games
            logger.info(f"Creating {len(match_import.games)} games for match {idx}...")
            for game_idx, game_import in enumerate(match_import.games, 1):
                logger.debug(f"Creating game {game_idx}: Game #{game_import.game_number}, winner={game_import.winner_name}")
                winner_id = player_map.get(game_import.winner_name)
                if not winner_id:
                    error_msg = f"Unknown winner in match {idx}, game {game_idx}: '{game_import.winner_name}'"
                    logger.error(error_msg)
                    raise HTTPException(
                        status_code=status.HTTP_400_BAD_REQUEST,
                        detail=error_msg
                    )
                
                try:
                    game_create = schemas.GameCreate(
                        game_number=game_import.game_number,
                        winner_id=winner_id,
                        game_result="WIN",
                        duration_minutes=game_import.duration_minutes
                    )
                    matches_crud.create_game(db, new_match.id, game_create)
                    logger.debug(f"Game {game_idx} created successfully")
                    created_games += 1
                except Exception as e:
                    logger.error(f"Failed to create game {game_idx} for match {idx}: {str(e)}")
                    logger.error(f"Game data: game_number={game_import.game_number}, winner_id={winner_id}, duration={game_import.duration_minutes}")
                    raise
        
        logger.info(f"Successfully processed all matches: {created_matches} matches, {created_games} games")
        
        return schemas.TournamentImportResponse(
            success=True,
            message=f"Successfully imported tournament '{new_tournament.name}'",
            tournament_id=new_tournament.id,
            tournament_created=True,
            players_created=created_players,
            decks_created=created_decks,
            matches_created=created_matches,
            games_created=created_games
        )
        
    except HTTPException:
        db.rollback()
        raise
    except Exception as e:
        db.rollback()
        error_trace = traceback.format_exc()
        logger.error(f"Tournament import failed with exception: {str(e)}")
        logger.error(f"Full traceback:\n{error_trace}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Error importing tournament: {type(e).__name__}: {str(e)}"
        )
