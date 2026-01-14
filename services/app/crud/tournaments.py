"""CRUD operations for Tournament model."""
from sqlalchemy.orm import Session
from sqlalchemy import desc
from app import models, schemas
from typing import Optional, List


def get_tournament(db: Session, tournament_id: int) -> Optional[models.Tournament]:
    """Get a tournament by ID."""
    return db.query(models.Tournament).filter(models.Tournament.id == tournament_id).first()


def get_tournaments(db: Session, skip: int = 0, limit: int = 100, season_id: Optional[int] = None) -> List[models.Tournament]:
    """Get list of tournaments."""
    query = db.query(models.Tournament)
    if season_id:
        query = query.filter(models.Tournament.season_id == season_id)
    return query.order_by(desc(models.Tournament.tournament_date)).offset(skip).limit(limit).all()


def create_tournament(db: Session, tournament: schemas.TournamentCreate) -> models.Tournament:
    """Create a new tournament."""
    db_tournament = models.Tournament(**tournament.model_dump())
    db.add(db_tournament)
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def update_tournament(db: Session, tournament_id: int, tournament: schemas.TournamentUpdate) -> Optional[models.Tournament]:
    """Update a tournament."""
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        return None
    
    update_data = tournament.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tournament, field, value)
    
    db.commit()
    db.refresh(db_tournament)
    return db_tournament


def delete_tournament(db: Session, tournament_id: int) -> bool:
    """Delete a tournament."""
    db_tournament = get_tournament(db, tournament_id)
    if not db_tournament:
        return False
    
    db.delete(db_tournament)
    db.commit()
    return True
