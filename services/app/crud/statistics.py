"""CRUD operations for statistics queries using database views."""
from sqlalchemy.orm import Session
from sqlalchemy import text
from app import schemas
from typing import List, Optional


def get_player_statistics(db: Session) -> List[schemas.PlayerStatistics]:
    """Get statistics for all players from player_statistics view."""
    query = text("""
        SELECT 
            player_id, player_name, total_matches, matches_won, 
            matches_drawn, matches_lost, win_rate_percentage,
            decks_played, tournaments_played
        FROM player_statistics
        ORDER BY win_rate_percentage DESC NULLS LAST, matches_won DESC
    """)
    
    result = db.execute(query)
    rows = result.fetchall()
    
    return [
        schemas.PlayerStatistics(
            player_id=row[0],
            player_name=row[1],
            total_matches=row[2],
            matches_won=row[3],
            matches_drawn=row[4],
            matches_lost=row[5],
            win_rate_percentage=row[6],
            decks_played=row[7],
            tournaments_played=row[8]
        )
        for row in rows
    ]


def get_player_statistics_by_id(db: Session, player_id: int) -> Optional[schemas.PlayerStatistics]:
    """Get statistics for a specific player."""
    query = text("""
        SELECT 
            player_id, player_name, total_matches, matches_won, 
            matches_drawn, matches_lost, win_rate_percentage,
            decks_played, tournaments_played
        FROM player_statistics
        WHERE player_id = :player_id
    """)
    
    result = db.execute(query, {"player_id": player_id})
    row = result.fetchone()
    
    if not row:
        return None
    
    return schemas.PlayerStatistics(
        player_id=row[0],
        player_name=row[1],
        total_matches=row[2],
        matches_won=row[3],
        matches_drawn=row[4],
        matches_lost=row[5],
        win_rate_percentage=row[6],
        decks_played=row[7],
        tournaments_played=row[8]
    )


def get_deck_statistics(db: Session) -> List[schemas.DeckStatistics]:
    """Get statistics for all deck archetypes from deck_statistics view."""
    query = text("""
        SELECT 
            deck_id, deck_name, color_identity, archetype_type,
            total_matches, matches_won, matches_drawn, matches_lost,
            win_rate_percentage, unique_players, tournaments_played
        FROM deck_statistics
        ORDER BY win_rate_percentage DESC NULLS LAST, matches_won DESC
    """)
    
    result = db.execute(query)
    rows = result.fetchall()
    
    return [
        schemas.DeckStatistics(
            deck_id=row[0],
            deck_name=row[1],
            color_identity=row[2],
            archetype_type=row[3],
            total_matches=row[4],
            matches_won=row[5],
            matches_drawn=row[6],
            matches_lost=row[7],
            win_rate_percentage=row[8],
            unique_players=row[9],
            tournaments_played=row[10]
        )
        for row in rows
    ]


def get_deck_statistics_by_id(db: Session, deck_id: int) -> Optional[schemas.DeckStatistics]:
    """Get statistics for a specific deck archetype."""
    query = text("""
        SELECT 
            deck_id, deck_name, color_identity, archetype_type,
            total_matches, matches_won, matches_drawn, matches_lost,
            win_rate_percentage, unique_players, tournaments_played
        FROM deck_statistics
        WHERE deck_id = :deck_id
    """)
    
    result = db.execute(query, {"deck_id": deck_id})
    row = result.fetchone()
    
    if not row:
        return None
    
    return schemas.DeckStatistics(
        deck_id=row[0],
        deck_name=row[1],
        color_identity=row[2],
        archetype_type=row[3],
        total_matches=row[4],
        matches_won=row[5],
        matches_drawn=row[6],
        matches_lost=row[7],
        win_rate_percentage=row[8],
        unique_players=row[9],
        tournaments_played=row[10]
    )


def get_deck_matchups(db: Session) -> List[schemas.DeckMatchup]:
    """Get matchup statistics for all deck pairings."""
    query = text("""
        SELECT 
            deck_a_id, deck_a_name, deck_b_id, deck_b_name,
            total_matches, deck_a_wins, draws, deck_a_losses,
            deck_a_win_rate_percentage, deck_b_win_rate_percentage
        FROM deck_matchups
        ORDER BY total_matches DESC, deck_a_win_rate_percentage DESC NULLS LAST
    """)
    
    result = db.execute(query)
    rows = result.fetchall()
    
    return [
        schemas.DeckMatchup(
            deck_a_id=row[0],
            deck_a_name=row[1],
            deck_b_id=row[2],
            deck_b_name=row[3],
            total_matches=row[4],
            deck_a_wins=row[5],
            draws=row[6],
            deck_a_losses=row[7],
            deck_a_win_rate_percentage=row[8],
            deck_b_win_rate_percentage=row[9]
        )
        for row in rows
    ]


def get_deck_matchup(db: Session, deck_a_id: int, deck_b_id: int) -> Optional[schemas.DeckMatchup]:
    """Get matchup statistics for a specific deck pairing."""
    query = text("""
        SELECT 
            deck_a_id, deck_a_name, deck_b_id, deck_b_name,
            total_matches, deck_a_wins, draws, deck_a_losses,
            deck_a_win_rate_percentage, deck_b_win_rate_percentage
        FROM deck_matchups
        WHERE (deck_a_id = :deck_a_id AND deck_b_id = :deck_b_id)
           OR (deck_a_id = :deck_b_id AND deck_b_id = :deck_a_id)
        LIMIT 1
    """)
    
    result = db.execute(query, {"deck_a_id": deck_a_id, "deck_b_id": deck_b_id})
    row = result.fetchone()
    
    if not row:
        return None
    
    return schemas.DeckMatchup(
        deck_a_id=row[0],
        deck_a_name=row[1],
        deck_b_id=row[2],
        deck_b_name=row[3],
        total_matches=row[4],
        deck_a_wins=row[5],
        draws=row[6],
        deck_a_losses=row[7],
        deck_a_win_rate_percentage=row[8],
        deck_b_win_rate_percentage=row[9]
    )


def get_season_standings(db: Session, season_id: Optional[int] = None) -> List[schemas.SeasonStandings]:
    """Get season standings for all seasons or a specific season."""
    if season_id:
        query = text("""
            SELECT 
                season_id, season_name, player_id, player_name,
                matches_played, wins, draws, losses, points
            FROM season_standings
            WHERE season_id = :season_id
            ORDER BY points DESC, wins DESC, player_name
        """)
        result = db.execute(query, {"season_id": season_id})
    else:
        query = text("""
            SELECT 
                season_id, season_name, player_id, player_name,
                matches_played, wins, draws, losses, points
            FROM season_standings
            ORDER BY season_id, points DESC, wins DESC, player_name
        """)
        result = db.execute(query)
    
    rows = result.fetchall()
    
    return [
        schemas.SeasonStandings(
            season_id=row[0],
            season_name=row[1],
            player_id=row[2],
            player_name=row[3],
            matches_played=row[4],
            wins=row[5],
            draws=row[6],
            losses=row[7],
            points=row[8]
        )
        for row in rows
    ]
