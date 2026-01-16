"""CRUD operations for Tournament model."""
from sqlalchemy.orm import Session
from sqlalchemy import desc, func
from app import models, schemas
from typing import Optional, List

DEFAULT_TOURNAMENT_TYPE_NAME = "LGS Tournament"


def get_tournament_type_by_id(db: Session, type_id: int) -> Optional[models.TournamentType]:
    """Get tournament type by ID."""
    return db.query(models.TournamentType).filter(models.TournamentType.id == type_id).first()


def get_tournament_type_by_name(db: Session, name: str) -> Optional[models.TournamentType]:
    """Get tournament type by unique name (case-insensitive)."""
    return (
        db.query(models.TournamentType)
        .filter(func.lower(models.TournamentType.name) == func.lower(name))
        .first()
    )


def resolve_tournament_type(db: Session, type_id: Optional[int], type_name: Optional[str]) -> models.TournamentType:
    """Resolve tournament type using id or name; fallback to default type when neither provided."""
    resolved = None
    if type_id is not None:
        resolved = get_tournament_type_by_id(db, type_id)
        if not resolved:
            raise ValueError(f"Tournament type with id {type_id} not found")
    if type_name:
        by_name = get_tournament_type_by_name(db, type_name)
        if not by_name:
            raise ValueError(f"Tournament type '{type_name}' not found")
        if resolved and resolved.id != by_name.id:
            raise ValueError("Provided tournament_type_id does not match tournament_type_name")
        resolved = by_name
    if not resolved:
        resolved = get_tournament_type_by_name(db, DEFAULT_TOURNAMENT_TYPE_NAME)
        if not resolved:
            raise ValueError(f"Default tournament type '{DEFAULT_TOURNAMENT_TYPE_NAME}' not found")
    return resolved


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
    tournament_type = resolve_tournament_type(
        db,
        tournament.tournament_type_id,
        tournament.tournament_type_name,
    )
    payload = tournament.model_dump(exclude={"tournament_type_name"}, exclude_none=True)
    payload["tournament_type_id"] = tournament_type.id
    db_tournament = models.Tournament(**payload)
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
    type_id = update_data.pop("tournament_type_id", None)
    type_name = update_data.pop("tournament_type_name", None)

    if type_id is not None or type_name is not None:
        tournament_type = resolve_tournament_type(db, type_id, type_name)
        update_data["tournament_type_id"] = tournament_type.id
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
