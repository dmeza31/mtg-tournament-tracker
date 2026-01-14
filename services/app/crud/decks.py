"""CRUD operations for DeckArchetype model."""
from sqlalchemy.orm import Session
from app import models, schemas
from typing import Optional, List


def get_deck_archetype(db: Session, deck_id: int) -> Optional[models.DeckArchetype]:
    """Get a deck archetype by ID."""
    return db.query(models.DeckArchetype).filter(models.DeckArchetype.id == deck_id).first()


def get_deck_archetype_by_name(db: Session, name: str) -> Optional[models.DeckArchetype]:
    """Get a deck archetype by name."""
    return db.query(models.DeckArchetype).filter(models.DeckArchetype.name == name).first()


def get_deck_by_name(db: Session, name: str) -> Optional[models.DeckArchetype]:
    """Alias for get_deck_archetype_by_name."""
    return get_deck_archetype_by_name(db, name)


def get_deck_archetypes(db: Session, skip: int = 0, limit: int = 100, archetype_type: Optional[str] = None) -> List[models.DeckArchetype]:
    """Get list of deck archetypes."""
    query = db.query(models.DeckArchetype)
    if archetype_type:
        query = query.filter(models.DeckArchetype.archetype_type == archetype_type)
    return query.order_by(models.DeckArchetype.name).offset(skip).limit(limit).all()


def create_deck_archetype(db: Session, deck: schemas.DeckArchetypeCreate) -> models.DeckArchetype:
    """Create a new deck archetype."""
    db_deck = models.DeckArchetype(**deck.model_dump())
    db.add(db_deck)
    db.commit()
    db.refresh(db_deck)
    return db_deck


def update_deck_archetype(db: Session, deck_id: int, deck: schemas.DeckArchetypeUpdate) -> Optional[models.DeckArchetype]:
    """Update a deck archetype."""
    db_deck = get_deck_archetype(db, deck_id)
    if not db_deck:
        return None
    
    update_data = deck.model_dump(exclude_unset=True)
    for field, value in update_data.items():
        setattr(db_deck, field, value)
    
    db.commit()
    db.refresh(db_deck)
    return db_deck


def delete_deck_archetype(db: Session, deck_id: int) -> bool:
    """Delete a deck archetype."""
    db_deck = get_deck_archetype(db, deck_id)
    if not db_deck:
        return False
    
    db.delete(db_deck)
    db.commit()
    return True
