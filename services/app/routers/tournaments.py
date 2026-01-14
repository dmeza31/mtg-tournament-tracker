"""Router for Tournament endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas
from app.database import get_db
from app.crud import tournaments

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
    return tournaments.create_tournament(db=db, tournament=tournament)


@router.put("/{tournament_id}", response_model=schemas.Tournament)
def update_tournament(
    tournament_id: int,
    tournament: schemas.TournamentUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing tournament."""
    db_tournament = tournaments.update_tournament(db, tournament_id=tournament_id, tournament=tournament)
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
