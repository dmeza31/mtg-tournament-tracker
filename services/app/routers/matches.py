"""Router for Match and Game endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas
from app.database import get_db
from app.crud import matches

router = APIRouter(prefix="/matches", tags=["Matches & Games"])


@router.get("/", response_model=List[schemas.Match])
def list_matches(
    skip: int = 0,
    limit: int = 100,
    tournament_id: Optional[int] = Query(None, description="Filter by tournament ID"),
    player_id: Optional[int] = Query(None, description="Filter by player ID"),
    db: Session = Depends(get_db)
):
    """
    Get list of all matches.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **tournament_id**: Optional filter by tournament
    - **player_id**: Optional filter by player (either player1 or player2)
    """
    return matches.get_matches(
        db, 
        skip=skip, 
        limit=limit, 
        tournament_id=tournament_id,
        player_id=player_id
    )


@router.get("/{match_id}", response_model=schemas.MatchWithGames)
def get_match(match_id: int, db: Session = Depends(get_db)):
    """Get a specific match by ID with all its games."""
    db_match = matches.get_match(db, match_id=match_id)
    if not db_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    return db_match


@router.post("/", response_model=schemas.Match, status_code=status.HTTP_201_CREATED)
def create_match(match: schemas.MatchCreate, db: Session = Depends(get_db)):
    """
    Create a new match.
    
    - **tournament_id**: Tournament ID (required)
    - **player1_id**: First player ID (required)
    - **player2_id**: Second player ID (required, must be different from player1)
    - **player1_deck_id**: First player's deck archetype ID (required)
    - **player2_deck_id**: Second player's deck archetype ID (required)
    - **round_number**: Tournament round (optional)
    - **match_status**: Status (default: COMPLETED)
    - **notes**: Match notes (optional)
    
    Note: Games should be added separately or use batch endpoint.
    """
    return matches.create_match(db=db, match=match)


@router.put("/{match_id}", response_model=schemas.Match)
def update_match(
    match_id: int,
    match: schemas.MatchUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing match."""
    db_match = matches.update_match(db, match_id=match_id, match=match)
    if not db_match:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    return db_match


@router.delete("/{match_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_match(match_id: int, db: Session = Depends(get_db)):
    """Delete a match (and all its games)."""
    if not matches.delete_match(db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    return None


# Game endpoints

@router.get("/{match_id}/games", response_model=List[schemas.Game])
def list_games_for_match(match_id: int, db: Session = Depends(get_db)):
    """Get all games for a specific match."""
    # Check if match exists
    if not matches.get_match(db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    return matches.get_games_by_match(db, match_id=match_id)


@router.post("/{match_id}/games", response_model=schemas.Game, status_code=status.HTTP_201_CREATED)
def create_game(match_id: int, game: schemas.GameCreate, db: Session = Depends(get_db)):
    """
    Create a new game for a match.
    
    - **game_number**: Game number (1-3)
    - **winner_id**: Player ID who won
    - **game_result**: Result (WIN or DRAW)
    - **duration_minutes**: Game duration (optional)
    - **notes**: Game notes (optional)
    """
    # Check if match exists
    if not matches.get_match(db, match_id=match_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Match with id {match_id} not found"
        )
    
    try:
        return matches.create_game(db=db, match_id=match_id, game=game)
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Error creating game: {str(e)}"
        )


@router.put("/{match_id}/games/{game_id}", response_model=schemas.Game)
def update_game(match_id: int, game_id: int, game: schemas.GameUpdate, db: Session = Depends(get_db)):
    """Update a game for a match."""
    db_game = matches.get_game(db, game_id=game_id)
    if not db_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with id {game_id} not found"
        )
    if db_game.match_id != match_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game {game_id} does not belong to match {match_id}"
        )
    updated = matches.update_game(db, game_id=game_id, game=game)
    return updated


@router.delete("/{match_id}/games/{game_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_game(match_id: int, game_id: int, db: Session = Depends(get_db)):
    """Delete a game."""
    db_game = matches.get_game(db, game_id=game_id)
    if not db_game:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Game with id {game_id} not found"
        )
    
    if db_game.match_id != match_id:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail=f"Game {game_id} does not belong to match {match_id}"
        )
    
    matches.delete_game(db, game_id=game_id)
    return None


# Batch endpoint

@router.post("/batch", response_model=schemas.BatchMatchResponse, status_code=status.HTTP_201_CREATED)
def batch_create_matches(batch: schemas.BatchMatchCreate, db: Session = Depends(get_db)):
    """
    Create multiple matches with their games in a single transaction.
    
    This endpoint allows you to insert multiple complete matches (with games) at once.
    Each match is processed independently - if one fails, others can still succeed.
    
    Request body should contain:
    - **matches**: Array of match objects, each containing:
      - Match details (tournament_id, players, decks, etc.)
      - **games**: Array of 1-3 games with winner and result
    
    Returns:
    - **success_count**: Number of successfully created matches
    - **failed_count**: Number of failed matches
    - **created_match_ids**: IDs of successfully created matches
    - **errors**: Details of any failures
    """
    return matches.batch_create_matches(db, matches=batch.matches)
