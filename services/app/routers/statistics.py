"""Router for Statistics endpoints."""
from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List, Optional
from app import schemas
from app.database import get_db
from app.crud import statistics

router = APIRouter(prefix="/stats", tags=["Statistics"])


@router.get("/players", response_model=List[schemas.PlayerStatistics])
def get_player_statistics(db: Session = Depends(get_db)):
    """
    Get statistics for all players.
    
    Returns wins, draws, losses, win rate, and other metrics for each player.
    Data is sourced from the `player_statistics` database view.
    """
    return statistics.get_player_statistics(db)


@router.get("/players/{player_id}", response_model=schemas.PlayerStatistics)
def get_player_statistics_by_id(player_id: int, db: Session = Depends(get_db)):
    """
    Get statistics for a specific player.
    
    Returns detailed performance metrics for the specified player.
    """
    stats = statistics.get_player_statistics_by_id(db, player_id=player_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No statistics found for player {player_id}"
        )
    return stats


@router.get("/decks", response_model=List[schemas.DeckStatistics])
def get_deck_statistics(db: Session = Depends(get_db)):
    """
    Get statistics for all deck archetypes.
    
    Returns wins, draws, losses, win rate, and other metrics for each deck.
    Data is sourced from the `deck_statistics` database view.
    """
    return statistics.get_deck_statistics(db)


@router.get("/decks/{deck_id}", response_model=schemas.DeckStatistics)
def get_deck_statistics_by_id(deck_id: int, db: Session = Depends(get_db)):
    """
    Get statistics for a specific deck archetype.
    
    Returns detailed performance metrics for the specified deck.
    """
    stats = statistics.get_deck_statistics_by_id(db, deck_id=deck_id)
    if not stats:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No statistics found for deck {deck_id}"
        )
    return stats


@router.get("/matchups", response_model=List[schemas.DeckMatchup])
def get_deck_matchups(db: Session = Depends(get_db)):
    """
    Get matchup statistics for all deck pairings.
    
    Returns head-to-head performance data for deck archetypes.
    Shows total matches, wins for each deck, and win rates.
    Data is sourced from the `deck_matchups` database view.
    """
    return statistics.get_deck_matchups(db)


@router.get("/matchups/{deck_a_id}/{deck_b_id}", response_model=schemas.DeckMatchup)
def get_deck_matchup(deck_a_id: int, deck_b_id: int, db: Session = Depends(get_db)):
    """
    Get matchup statistics for a specific deck pairing.
    
    Returns head-to-head performance between two specific deck archetypes.
    Example: How does Mono Red Aggro perform against Azorius Control?
    
    - **deck_a_id**: First deck archetype ID
    - **deck_b_id**: Second deck archetype ID
    """
    matchup = statistics.get_deck_matchup(db, deck_a_id=deck_a_id, deck_b_id=deck_b_id)
    if not matchup:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No matchup data found for decks {deck_a_id} vs {deck_b_id}"
        )
    return matchup


@router.get("/season-standings", response_model=List[schemas.SeasonStandings])
def get_season_standings(season_id: Optional[int] = None, db: Session = Depends(get_db)):
    """
    Get player standings by season with points.
    
    Points are calculated as:
    - 3 points per win
    - 1 point per draw
    
    Results are ordered by points (descending), then wins (descending).
    
    - **season_id** (optional): Filter standings for a specific season
    """
    return statistics.get_season_standings(db, season_id=season_id)


@router.get("/season-standings/{season_id}", response_model=List[schemas.SeasonStandings])
def get_season_standings_by_id(season_id: int, db: Session = Depends(get_db)):
    """
    Get player standings for a specific season.
    
    Returns the standings table with player names and points,
    ordered by points descending.
    """
    standings = statistics.get_season_standings(db, season_id=season_id)
    if not standings:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"No standings found for season {season_id}"
        )
    return standings
