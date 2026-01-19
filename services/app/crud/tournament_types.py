"""CRUD operations for TournamentType model."""
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List


def get_tournament_type(db: Session, tournament_type_id: int) -> Optional[models.TournamentType]:
    """Get a tournament type by ID."""
    return db.query(models.TournamentType).filter(models.TournamentType.id == tournament_type_id).first()


def get_tournament_types(db: Session, skip: int = 0, limit: int = 100) -> List[models.TournamentType]:
    """Get list of tournament types."""
    return db.query(models.TournamentType).order_by(models.TournamentType.name).offset(skip).limit(limit).all()


def create_tournament_type(db: Session, tournament_type: schemas.TournamentTypeCreate) -> models.TournamentType:
    """Create a new tournament type."""
    db_tournament_type = models.TournamentType(**tournament_type.model_dump())
    db.add(db_tournament_type)
    db.commit()
    db.refresh(db_tournament_type)
    return db_tournament_type


def update_tournament_type(
    db: Session, tournament_type_id: int, tournament_type: schemas.TournamentTypeUpdate
) -> Optional[models.TournamentType]:
    """Update a tournament type."""
    db_tournament_type = get_tournament_type(db, tournament_type_id)
    if not db_tournament_type:
        return None
    
    update_data = tournament_type.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_tournament_type, field, value)
    
    db.commit()
    db.refresh(db_tournament_type)
    return db_tournament_type


def delete_tournament_type(db: Session, tournament_type_id: int) -> bool:
    """Delete a tournament type."""
    db_tournament_type = get_tournament_type(db, tournament_type_id)
    if not db_tournament_type:
        return False
    
    db.delete(db_tournament_type)
    db.commit()
    return True
