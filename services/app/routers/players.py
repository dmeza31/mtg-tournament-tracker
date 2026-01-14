"""Router for Player endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.crud import players

router = APIRouter(prefix="/players", tags=["Players"])


@router.get("/", response_model=List[schemas.Player])
def list_players(
    skip: int = 0,
    limit: int = 100,
    active_only: bool = Query(False, description="Show only active players"),
    db: Session = Depends(get_db)
):
    """
    Get list of all players.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **active_only**: Filter to show only active players
    """
    return players.get_players(db, skip=skip, limit=limit, active_only=active_only)


@router.get("/{player_id}", response_model=schemas.Player)
def get_player(player_id: int, db: Session = Depends(get_db)):
    """Get a specific player by ID."""
    db_player = players.get_player(db, player_id=player_id)
    if not db_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found"
        )
    return db_player


@router.post("/", response_model=schemas.Player, status_code=status.HTTP_201_CREATED)
def create_player(player: schemas.PlayerCreate, db: Session = Depends(get_db)):
    """
    Create a new player.
    
    - **name**: Player name (required)
    - **email**: Player email (optional, must be unique)
    - **active**: Whether player is active (default: true)
    - **notes**: Player notes (optional)
    """
    # Check if email already exists
    if player.email:
        db_player = players.get_player_by_email(db, email=player.email)
        if db_player:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"Player with email {player.email} already exists"
            )
    
    return players.create_player(db=db, player=player)


@router.put("/{player_id}", response_model=schemas.Player)
def update_player(
    player_id: int,
    player: schemas.PlayerUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing player."""
    db_player = players.update_player(db, player_id=player_id, player=player)
    if not db_player:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Player with id {player_id} not found"
        )
    return db_player


@router.delete("/{player_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_player(player_id: int, db: Session = Depends(get_db)):
    """
    Delete a player.
    
    Note: Cannot delete if player has participated in matches (foreign key constraint).
    """
    try:
        if not players.delete_player(db, player_id=player_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Player with id {player_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete player: {str(e)}"
        )
    return None
