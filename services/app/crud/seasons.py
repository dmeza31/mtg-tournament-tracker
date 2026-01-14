"""CRUD operations for Season model."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import models, schemas
from typing import Optional, List


def get_season(db: Session, season_id: int) -> Optional[models.Season]:
    """Get a season by ID."""
    return db.query(models.Season).filter(models.Season.id == season_id).first()


def get_seasons(db: Session, skip: int = 0, limit: int = 100) -> List[models.Season]:
    """Get list of seasons."""
    return db.query(models.Season).order_by(desc(models.Season.start_date)).offset(skip).limit(limit).all()


def create_season(db: Session, season: schemas.SeasonCreate) -> models.Season:
    """Create a new season."""
    db_season = models.Season(**season.model_dump())
    db.add(db_season)
    db.commit()
    db.refresh(db_season)
    return db_season


def update_season(db: Session, season_id: int, season: schemas.SeasonUpdate) -> Optional[models.Season]:
    """Update a season."""
    db_season = get_season(db, season_id)
    if not db_season:
        return None
    
    update_data = season.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_season, field, value)
    
    db.commit()
    db.refresh(db_season)
    return db_season


def delete_season(db: Session, season_id: int) -> bool:
    """Delete a season."""
    db_season = get_season(db, season_id)
    if not db_season:
        return False
    
    db.delete(db_season)
    db.commit()
    return True
