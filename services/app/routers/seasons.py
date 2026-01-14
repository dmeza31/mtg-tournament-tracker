"""Router for Season endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List
from app import schemas
from app.database import get_db
from app.crud import seasons

router = APIRouter(prefix="/seasons", tags=["Seasons"])


@router.get("/", response_model=List[schemas.Season])
def list_seasons(
    skip: int = 0,
    limit: int = 100,
    db: Session = Depends(get_db)
):
    """
    Get list of all seasons.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    """
    return seasons.get_seasons(db, skip=skip, limit=limit)


@router.get("/{season_id}", response_model=schemas.Season)
def get_season(season_id: int, db: Session = Depends(get_db)):
    """Get a specific season by ID."""
    db_season = seasons.get_season(db, season_id=season_id)
    if not db_season:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found"
        )
    return db_season


@router.post("/", response_model=schemas.Season, status_code=status.HTTP_201_CREATED)
def create_season(season: schemas.SeasonCreate, db: Session = Depends(get_db)):
    """
    Create a new season.
    
    - **name**: Season name (required, unique)
    - **start_date**: Season start date (required)
    - **end_date**: Season end date (optional)
    - **description**: Season description (optional)
    """
    return seasons.create_season(db=db, season=season)


@router.put("/{season_id}", response_model=schemas.Season)
def update_season(
    season_id: int,
    season: schemas.SeasonUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing season."""
    db_season = seasons.update_season(db, season_id=season_id, season=season)
    if not db_season:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found"
        )
    return db_season


@router.delete("/{season_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_season(season_id: int, db: Session = Depends(get_db)):
    """Delete a season (and all its tournaments)."""
    if not seasons.delete_season(db, season_id=season_id):
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Season with id {season_id} not found"
        )
    return None
