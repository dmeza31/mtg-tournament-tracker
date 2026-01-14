"""CRUD operations for Player model."""
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List


def get_player(db: Session, player_id: int) -> Optional[models.Player]:
    """Get a player by ID."""
    return db.query(models.Player).filter(models.Player.id == player_id).first()


def get_player_by_email(db: Session, email: str) -> Optional[models.Player]:
    """Get a player by email."""
    return db.query(models.Player).filter(models.Player.email == email).first()


def get_player_by_name(db: Session, name: str) -> Optional[models.Player]:
    """Get a player by name."""
    return db.query(models.Player).filter(models.Player.name == name).first()


def get_players(db: Session, skip: int = 0, limit: int = 100, active_only: bool = False) -> List[models.Player]:
    """Get list of players."""
    query = db.query(models.Player)
    if active_only:
        query = query.filter(models.Player.active == True)
    return query.order_by(models.Player.name).offset(skip).limit(limit).all()


def create_player(db: Session, player: schemas.PlayerCreate) -> models.Player:
    """Create a new player."""
    db_player = models.Player(**player.model_dump())
    db.add(db_player)
    db.commit()
    db.refresh(db_player)
    return db_player


def update_player(db: Session, player_id: int, player: schemas.PlayerUpdate) -> Optional[models.Player]:
    """Update a player."""
    db_player = get_player(db, player_id)
    if not db_player:
        return None
    
    update_data = player.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_player, field, value)
    
    db.commit()
    db.refresh(db_player)
    return db_player


def delete_player(db: Session, player_id: int) -> bool:
    """Delete a player."""
    db_player = get_player(db, player_id)
    if not db_player:
        return False
    
    db.delete(db_player)
    db.commit()
    return True
