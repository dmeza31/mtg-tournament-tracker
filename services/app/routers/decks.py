"""Router for Deck Archetype endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas
from app.database import get_db
from app.crud import decks

router = APIRouter(prefix="/decks", tags=["Deck Archetypes"])


@router.get("/", response_model=List[schemas.DeckArchetype])
def list_deck_archetypes(
    skip: int = 0,
    limit: int = 100,
    archetype_type: Optional[str] = Query(None, description="Filter by archetype type"),
    db: Session = Depends(get_db)
):
    """
    Get list of all deck archetypes.
    
    - **skip**: Number of records to skip (for pagination)
    - **limit**: Maximum number of records to return
    - **archetype_type**: Optional filter by type (Aggro, Control, etc.)
    """
    return decks.get_deck_archetypes(db, skip=skip, limit=limit, archetype_type=archetype_type)


@router.get("/{deck_id}", response_model=schemas.DeckArchetype)
def get_deck_archetype(deck_id: int, db: Session = Depends(get_db)):
    """Get a specific deck archetype by ID."""
    db_deck = decks.get_deck_archetype(db, deck_id=deck_id)
    if not db_deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deck archetype with id {deck_id} not found"
        )
    return db_deck


@router.post("/", response_model=schemas.DeckArchetype, status_code=status.HTTP_201_CREATED)
def create_deck_archetype(deck: schemas.DeckArchetypeCreate, db: Session = Depends(get_db)):
    """
    Create a new deck archetype.
    
    - **name**: Deck archetype name (required, unique) - e.g., "Mono Red Aggro"
    - **color_identity**: WUBRG color combination (optional) - e.g., "R", "UW"
    - **archetype_type**: Type like Aggro, Control, Midrange (optional)
    - **description**: Deck description (optional)
    """
    # Check if name already exists
    db_deck = decks.get_deck_archetype_by_name(db, name=deck.name)
    if db_deck:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Deck archetype with name '{deck.name}' already exists"
        )
    
    return decks.create_deck_archetype(db=db, deck=deck)


@router.put("/{deck_id}", response_model=schemas.DeckArchetype)
def update_deck_archetype(
    deck_id: int,
    deck: schemas.DeckArchetypeUpdate,
    db: Session = Depends(get_db)
):
    """Update an existing deck archetype."""
    db_deck = decks.update_deck_archetype(db, deck_id=deck_id, deck=deck)
    if not db_deck:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Deck archetype with id {deck_id} not found"
        )
    return db_deck


@router.delete("/{deck_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_deck_archetype(deck_id: int, db: Session = Depends(get_db)):
    """
    Delete a deck archetype.
    
    Note: Cannot delete if deck is used in matches (foreign key constraint).
    """
    try:
        if not decks.delete_deck_archetype(db, deck_id=deck_id):
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Deck archetype with id {deck_id} not found"
            )
    except Exception as e:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT,
            detail=f"Cannot delete deck archetype: {str(e)}"
        )
    return None
