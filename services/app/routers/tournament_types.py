"""Router for Tournament Type endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
import logging

from app import schemas
from app.database import get_db
from app.crud import tournament_types

logger = logging.getLogger(__name__)

router = APIRouter(prefix="/tournament-types", tags=["Tournament Types"])


@router.get("/", response_model=List[schemas.TournamentType])
def list_tournament_types(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all tournament types.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    return tournament_types.get_tournament_types(db, skip=skip, limit=limit)


@router.get("/{tournament_type_id}", response_model=schemas.TournamentType)
def get_tournament_type(tournament_type_id: int, db: Session = Depends(get_db)):
    """Get a specific tournament type by ID."""
    db_tournament_type = tournament_types.get_tournament_type(db, tournament_type_id=tournament_type_id)
    if not db_tournament_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament type with id {tournament_type_id} not found"
        )
    return db_tournament_type


@router.post("/", response_model=schemas.TournamentType, status_code=status.HTTP_201_CREATED)
def create_tournament_type(tournament_type: schemas.TournamentTypeCreate, db: Session = Depends(get_db)):
    """
    Create a new tournament type.
    
    - **name**: Unique tournament type name (required)
    - **points_win**: Points awarded for a match win (required)
    - **points_draw**: Points awarded for a match draw (required)
    - **description**: Tournament type description (optional)
    """
    try:
        return tournament_types.create_tournament_type(db=db, tournament_type=tournament_type)
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))


@router.put("/{tournament_type_id}", response_model=schemas.TournamentType)
def update_tournament_type(
    tournament_type_id: int,
    tournament_type: schemas.TournamentTypeUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing tournament type."""
    try:
        db_tournament_type = tournament_types.update_tournament_type(
            db, tournament_type_id=tournament_type_id, tournament_type=tournament_type
        )
    except ValueError as exc:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(exc))
    if not db_tournament_type:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament type with id {tournament_type_id} not found"
        )
    return db_tournament_type


@router.delete("/{tournament_type_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_tournament_type(tournament_type_id: int, db: Session = Depends(get_db)):
    """Delete a tournament type."""
    success = tournament_types.delete_tournament_type(db, tournament_type_id=tournament_type_id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Tournament type with id {tournament_type_id} not found"
        )
