"""CRUD operations for Match and Game models."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from sqlalchemy.exc import IntegrityError
from app import models, schemas
from typing import Optional, List, Tuple


def get_match(db: Session, match_id: int) -> Optional[models.Match]:
    """Get a match by ID with player and deck names populated."""
    match = db.query(models.Match).filter(models.Match.id == match_id).first()
    
    if not match:
        return None
    
    # Get player names
    player1 = db.query(models.Player).filter(models.Player.id == match.player1_id).first()
    player2 = db.query(models.Player).filter(models.Player.id == match.player2_id).first()
    
    # Get deck names
    deck1 = db.query(models.DeckArchetype).filter(models.DeckArchetype.id == match.player1_deck_id).first()
    deck2 = db.query(models.DeckArchetype).filter(models.DeckArchetype.id == match.player2_deck_id).first()
    
    # Attach to match object for serialization
    match.player1_name = player1.name if player1 else f"Player {match.player1_id}"
    match.player2_name = player2.name if player2 else f"Player {match.player2_id}"
    match.player1_deck_name = deck1.name if deck1 else f"Deck {match.player1_deck_id}"
    match.player2_deck_name = deck2.name if deck2 else f"Deck {match.player2_deck_id}"
    
    return match


def get_matches(
    db: Session, 
    skip: int = 0, 
    limit: int = 100,
    tournament_id: Optional[int] = None,
    player_id: Optional[int] = None
) -> List[models.Match]:
    """Get list of matches with player and deck names populated."""
    query = db.query(models.Match)
    
    if tournament_id:
        query = query.filter(models.Match.tournament_id == tournament_id)
    
    if player_id:
        query = query.filter(
            (models.Match.player1_id == player_id) | 
            (models.Match.player2_id == player_id)
        )
    
    matches = query.order_by(desc(models.Match.match_date)).offset(skip).limit(limit).all()
    
    # Populate player and deck names
    for match in matches:
        # Get player names
        player1 = db.query(models.Player).filter(models.Player.id == match.player1_id).first()
        player2 = db.query(models.Player).filter(models.Player.id == match.player2_id).first()
        
        # Get deck names
        deck1 = db.query(models.DeckArchetype).filter(models.DeckArchetype.id == match.player1_deck_id).first()
        deck2 = db.query(models.DeckArchetype).filter(models.DeckArchetype.id == match.player2_deck_id).first()
        
        # Attach to match object for serialization
        match.player1_name = player1.name if player1 else f"Player {match.player1_id}"
        match.player2_name = player2.name if player2 else f"Player {match.player2_id}"
        match.player1_deck_name = deck1.name if deck1 else f"Deck {match.player1_deck_id}"
        match.player2_deck_name = deck2.name if deck2 else f"Deck {match.player2_deck_id}"
    
    return matches


def create_match(db: Session, match: schemas.MatchCreate) -> models.Match:
    """Create a new match."""
    db_match = models.Match(**match.model_dump())
    db.add(db_match)
    db.commit()
    db.refresh(db_match)
    return db_match


def update_match(db: Session, match_id: int, match: schemas.MatchUpdate) -> Optional[models.Match]:
    """Update a match."""
    db_match = get_match(db, match_id)
    if not db_match:
        return None
    
    update_data = match.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_match, field, value)
    
    db.commit()
    db.refresh(db_match)
    return db_match


def delete_match(db: Session, match_id: int) -> bool:
    """Delete a match."""
    db_match = get_match(db, match_id)
    if not db_match:
        return False
    
    db.delete(db_match)
    db.commit()
    return True


# Game CRUD operations

def get_game(db: Session, game_id: int) -> Optional[models.Game]:
    """Get a game by ID."""
    return db.query(models.Game).filter(models.Game.id == game_id).first()


def get_games_by_match(db: Session, match_id: int) -> List[models.Game]:
    """Get all games for a match."""
    return db.query(models.Game).filter(models.Game.match_id == match_id).order_by(models.Game.game_number).all()


def create_game(db: Session, match_id: int, game: schemas.GameCreate) -> models.Game:
    """Create a new game."""
    db_game = models.Game(match_id=match_id, **game.model_dump())
    db.add(db_game)
    db.commit()
    db.refresh(db_game)
    return db_game


def delete_game(db: Session, game_id: int) -> bool:
    """Delete a game."""
    db_game = get_game(db, game_id)
    if not db_game:
        return False
    
    db.delete(db_game)
    db.commit()
    return True


# Batch operations

def create_match_with_games(
    db: Session, 
    match_data: schemas.MatchWithGamesCreate
) -> Tuple[Optional[models.Match], Optional[str]]:
    """
    Create a match with its games in a transaction.
    
    Returns:
        Tuple of (Match, error_message)
    """
    try:
        # Start transaction
        db.begin_nested()
        
        # Create match
        match_dict = match_data.model_dump(exclude={'games'})
        db_match = models.Match(**match_dict)
        db.add(db_match)
        db.flush()  # Get the match ID without committing
        
        # Create games
        for game_data in match_data.games:
            db_game = models.Game(
                match_id=db_match.id,
                **game_data.model_dump()
            )
            db.add(db_game)
        
        db.commit()
        db.refresh(db_match)
        return db_match, None
        
    except IntegrityError as e:
        db.rollback()
        error_msg = str(e.orig) if hasattr(e, 'orig') else str(e)
        return None, error_msg
    except Exception as e:
        db.rollback()
        return None, str(e)


def batch_create_matches(
    db: Session,
    matches: List[schemas.MatchWithGamesCreate]
) -> schemas.BatchMatchResponse:
    """
    Create multiple matches with games in batch.
    
    Returns:
        BatchMatchResponse with success/failure counts and details
    """
    created_ids = []
    errors = []
    
    for idx, match_data in enumerate(matches):
        db_match, error = create_match_with_games(db, match_data)
        
        if db_match:
            created_ids.append(db_match.id)
        else:
            errors.append({
                "index": idx,
                "match_data": {
                    "tournament_id": match_data.tournament_id,
                    "player1_id": match_data.player1_id,
                    "player2_id": match_data.player2_id,
                },
                "error": error
            })
    
    return schemas.BatchMatchResponse(
        success_count=len(created_ids),
        failed_count=len(errors),
        created_match_ids=created_ids,
        errors=errors
    )
