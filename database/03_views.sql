-- ============================================================================
-- MTG Tournament Tracking System - Views
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Views for common queries and reporting:
--              - Match results (aggregating best-of-3 games)
--              - Player statistics (wins/draws/losses by player)
--              - Deck statistics (wins/draws/losses by deck archetype)
--              - Deck matchup analysis (head-to-head performance)
-- ============================================================================

-- ============================================================================
-- VIEW: match_results
-- ============================================================================
-- Aggregates individual games to determine match winners and outcomes
-- for best-of-3 matches
DROP VIEW IF EXISTS match_results CASCADE;

CREATE VIEW match_results AS
WITH game_summary AS (
    SELECT 
        g.match_id,
        g.winner_id,
        g.game_result,
        COUNT(*) as games_count
    FROM games g
    GROUP BY g.match_id, g.winner_id, g.game_result
),
player_wins AS (
    SELECT 
        match_id,
        winner_id,
        SUM(CASE WHEN game_result = 'WIN' THEN games_count ELSE 0 END) as wins
    FROM game_summary
    GROUP BY match_id, winner_id
)
SELECT 
    m.id as match_id,
    m.tournament_id,
    m.player1_id,
    m.player2_id,
    m.player1_deck_id,
    m.player2_deck_id,
    m.round_number,
    m.match_date,
    m.match_status,
    -- Determine match winner (first to 2 wins)
    CASE 
        WHEN COALESCE(pw1.wins, 0) >= 2 THEN m.player1_id
        WHEN COALESCE(pw2.wins, 0) >= 2 THEN m.player2_id
        ELSE NULL
    END as match_winner_id,
    -- Match result from player1's perspective
    CASE 
        WHEN COALESCE(pw1.wins, 0) >= 2 THEN 'WIN'
        WHEN COALESCE(pw2.wins, 0) >= 2 THEN 'LOSS'
        WHEN m.match_status = 'COMPLETED' THEN 'DRAW'
        ELSE 'INCOMPLETE'
    END as player1_result,
    -- Match result from player2's perspective
    CASE 
        WHEN COALESCE(pw2.wins, 0) >= 2 THEN 'WIN'
        WHEN COALESCE(pw1.wins, 0) >= 2 THEN 'LOSS'
        WHEN m.match_status = 'COMPLETED' THEN 'DRAW'
        ELSE 'INCOMPLETE'
    END as player2_result,
    -- Game wins for each player
    COALESCE(pw1.wins, 0) as player1_game_wins,
    COALESCE(pw2.wins, 0) as player2_game_wins,
    -- Total games played in the match
    (SELECT COUNT(*) FROM games WHERE match_id = m.id) as total_games
FROM matches m
LEFT JOIN player_wins pw1 ON m.id = pw1.match_id AND m.player1_id = pw1.winner_id
LEFT JOIN player_wins pw2 ON m.id = pw2.match_id AND m.player2_id = pw2.winner_id;

COMMENT ON VIEW match_results IS 'Match outcomes derived from best-of-3 game results';

-- ============================================================================
-- VIEW: player_statistics
-- ============================================================================
-- Aggregates match results to show wins, draws, and losses for each player
DROP VIEW IF EXISTS player_statistics CASCADE;

CREATE VIEW player_statistics AS
WITH player_matches AS (
    -- Player 1 perspective
    SELECT 
        mr.player1_id as player_id,
        mr.player1_result as result,
        mr.player1_deck_id as deck_id,
        mr.match_id,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
    
    UNION ALL
    
    -- Player 2 perspective
    SELECT 
        mr.player2_id as player_id,
        mr.player2_result as result,
        mr.player2_deck_id as deck_id,
        mr.match_id,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
)
SELECT 
    p.id as player_id,
    p.name as player_name,
    COUNT(*) as total_matches,
    SUM(CASE WHEN pm.result = 'WIN' THEN 1 ELSE 0 END) as matches_won,
    SUM(CASE WHEN pm.result = 'DRAW' THEN 1 ELSE 0 END) as matches_drawn,
    SUM(CASE WHEN pm.result = 'LOSS' THEN 1 ELSE 0 END) as matches_lost,
    -- Win rate calculation
    ROUND(
        100.0 * SUM(CASE WHEN pm.result = 'WIN' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 
        2
    ) as win_rate_percentage,
    -- Number of unique decks played
    COUNT(DISTINCT pm.deck_id) as decks_played,
    -- Number of tournaments participated
    COUNT(DISTINCT pm.tournament_id) as tournaments_played
FROM players p
LEFT JOIN player_matches pm ON p.id = pm.player_id
WHERE p.active = TRUE
GROUP BY p.id, p.name;

COMMENT ON VIEW player_statistics IS 'Win/draw/loss statistics for each player';

-- ============================================================================
-- VIEW: deck_statistics
-- ============================================================================
-- Aggregates match results to show wins, draws, and losses for each deck archetype
DROP VIEW IF EXISTS deck_statistics CASCADE;

CREATE VIEW deck_statistics AS
WITH deck_matches AS (
    -- Deck from player 1 perspective
    SELECT 
        mr.player1_deck_id as deck_id,
        mr.player1_result as result,
        mr.match_id,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
    
    UNION ALL
    
    -- Deck from player 2 perspective
    SELECT 
        mr.player2_deck_id as deck_id,
        mr.player2_result as result,
        mr.match_id,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
)
SELECT 
    da.id as deck_id,
    da.name as deck_name,
    da.color_identity,
    da.archetype_type,
    COUNT(*) as total_matches,
    SUM(CASE WHEN dm.result = 'WIN' THEN 1 ELSE 0 END) as matches_won,
    SUM(CASE WHEN dm.result = 'DRAW' THEN 1 ELSE 0 END) as matches_drawn,
    SUM(CASE WHEN dm.result = 'LOSS' THEN 1 ELSE 0 END) as matches_lost,
    -- Win rate calculation
    ROUND(
        100.0 * SUM(CASE WHEN dm.result = 'WIN' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 
        2
    ) as win_rate_percentage,
    -- Number of unique players who played this deck
    COUNT(DISTINCT 
        CASE 
            WHEN mr.player1_deck_id = da.id THEN mr.player1_id
            WHEN mr.player2_deck_id = da.id THEN mr.player2_id
        END
    ) as unique_players,
    -- Number of tournaments where this deck appeared
    COUNT(DISTINCT dm.tournament_id) as tournaments_played
FROM deck_archetypes da
LEFT JOIN deck_matches dm ON da.id = dm.deck_id
LEFT JOIN match_results mr ON dm.match_id = mr.match_id
GROUP BY da.id, da.name, da.color_identity, da.archetype_type;

COMMENT ON VIEW deck_statistics IS 'Win/draw/loss statistics for each deck archetype';

-- ============================================================================
-- VIEW: deck_matchups
-- ============================================================================
-- Shows head-to-head performance between deck archetypes (Deck X vs Deck Y)
DROP VIEW IF EXISTS deck_matchups CASCADE;

CREATE VIEW deck_matchups AS
WITH matchup_results AS (
    -- Deck 1 perspective (player1_deck vs player2_deck)
    SELECT 
        mr.player1_deck_id as deck_a_id,
        mr.player2_deck_id as deck_b_id,
        mr.player1_result as deck_a_result,
        mr.match_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
    
    UNION ALL
    
    -- Deck 2 perspective (player2_deck vs player1_deck)
    SELECT 
        mr.player2_deck_id as deck_a_id,
        mr.player1_deck_id as deck_b_id,
        mr.player2_result as deck_a_result,
        mr.match_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
)
SELECT 
    da1.id as deck_a_id,
    da1.name as deck_a_name,
    da2.id as deck_b_id,
    da2.name as deck_b_name,
    COUNT(*) as total_matches,
    SUM(CASE WHEN mr.deck_a_result = 'WIN' THEN 1 ELSE 0 END) as deck_a_wins,
    SUM(CASE WHEN mr.deck_a_result = 'DRAW' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN mr.deck_a_result = 'LOSS' THEN 1 ELSE 0 END) as deck_a_losses,
    -- Win rate for deck_a against deck_b
    ROUND(
        100.0 * SUM(CASE WHEN mr.deck_a_result = 'WIN' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 
        2
    ) as deck_a_win_rate_percentage,
    -- Win rate for deck_b against deck_a
    ROUND(
        100.0 * SUM(CASE WHEN mr.deck_a_result = 'LOSS' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 
        2
    ) as deck_b_win_rate_percentage
FROM matchup_results mr
JOIN deck_archetypes da1 ON mr.deck_a_id = da1.id
JOIN deck_archetypes da2 ON mr.deck_b_id = da2.id
WHERE da1.id <= da2.id  -- Avoid duplicate matchups (A vs B and B vs A)
GROUP BY da1.id, da1.name, da2.id, da2.name
HAVING COUNT(*) > 0;

COMMENT ON VIEW deck_matchups IS 'Head-to-head matchup statistics between deck archetypes';

-- ============================================================================
-- VIEW: player_deck_performance
-- ============================================================================
-- Shows performance of each player with each deck they've played
DROP VIEW IF EXISTS player_deck_performance CASCADE;

CREATE VIEW player_deck_performance AS
WITH player_deck_matches AS (
    -- Player 1 perspective
    SELECT 
        mr.player1_id as player_id,
        mr.player1_deck_id as deck_id,
        mr.player1_result as result,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
    
    UNION ALL
    
    -- Player 2 perspective
    SELECT 
        mr.player2_id as player_id,
        mr.player2_deck_id as deck_id,
        mr.player2_result as result,
        mr.tournament_id
    FROM match_results mr
    WHERE mr.match_status = 'COMPLETED'
)
SELECT 
    p.id as player_id,
    p.name as player_name,
    da.id as deck_id,
    da.name as deck_name,
    COUNT(*) as total_matches,
    SUM(CASE WHEN pdm.result = 'WIN' THEN 1 ELSE 0 END) as matches_won,
    SUM(CASE WHEN pdm.result = 'DRAW' THEN 1 ELSE 0 END) as matches_drawn,
    SUM(CASE WHEN pdm.result = 'LOSS' THEN 1 ELSE 0 END) as matches_lost,
    -- Win rate calculation
    ROUND(
        100.0 * SUM(CASE WHEN pdm.result = 'WIN' THEN 1 ELSE 0 END) / 
        NULLIF(COUNT(*), 0), 
        2
    ) as win_rate_percentage,
    -- Number of tournaments with this player-deck combination
    COUNT(DISTINCT pdm.tournament_id) as tournaments_played
FROM players p
JOIN player_deck_matches pdm ON p.id = pdm.player_id
JOIN deck_archetypes da ON pdm.deck_id = da.id
GROUP BY p.id, p.name, da.id, da.name;

COMMENT ON VIEW player_deck_performance IS 'Performance statistics for each player-deck combination';

-- ============================================================================
-- VIEW: tournament_summary
-- ============================================================================
-- Provides summary statistics for each tournament
DROP VIEW IF EXISTS tournament_summary CASCADE;

CREATE VIEW tournament_summary AS
SELECT 
    t.id as tournament_id,
    t.name as tournament_name,
    t.tournament_date,
    t.location,
    t.format,
    s.name as season_name,
    COUNT(DISTINCT m.id) as total_matches,
    COUNT(DISTINCT m.player1_id) + COUNT(DISTINCT m.player2_id) as total_player_appearances,
    COUNT(DISTINCT CASE WHEN m.match_status = 'COMPLETED' THEN m.id END) as completed_matches,
    COUNT(DISTINCT m.player1_deck_id) + COUNT(DISTINCT m.player2_deck_id) as unique_deck_appearances
FROM tournaments t
JOIN seasons s ON t.season_id = s.id
LEFT JOIN matches m ON t.id = m.tournament_id
GROUP BY t.id, t.name, t.tournament_date, t.location, t.format, s.name;

COMMENT ON VIEW tournament_summary IS 'Summary statistics for each tournament';

-- ============================================================================
-- VIEW: season_standings
-- ============================================================================
-- Player standings by season with points (3 per win, 1 per draw)
DROP VIEW IF EXISTS season_standings CASCADE;

CREATE VIEW season_standings AS
WITH player_matches AS (
    -- Player 1 perspective
    SELECT 
        t.season_id,
        s.name as season_name,
        mr.player1_id as player_id,
        p.name as player_name,
        mr.player1_result as result
    FROM match_results mr
    JOIN matches m ON mr.match_id = m.id
    JOIN tournaments t ON mr.tournament_id = t.id
    JOIN seasons s ON t.season_id = s.id
    JOIN players p ON mr.player1_id = p.id
    WHERE mr.match_status = 'COMPLETED'
    
    UNION ALL
    
    -- Player 2 perspective
    SELECT 
        t.season_id,
        s.name as season_name,
        mr.player2_id as player_id,
        p.name as player_name,
        mr.player2_result as result
    FROM match_results mr
    JOIN matches m ON mr.match_id = m.id
    JOIN tournaments t ON mr.tournament_id = t.id
    JOIN seasons s ON t.season_id = s.id
    JOIN players p ON mr.player2_id = p.id
    WHERE mr.match_status = 'COMPLETED'
)
SELECT 
    season_id,
    season_name,
    player_id,
    player_name,
    COUNT(*) as matches_played,
    SUM(CASE WHEN result = 'WIN' THEN 1 ELSE 0 END) as wins,
    SUM(CASE WHEN result = 'DRAW' THEN 1 ELSE 0 END) as draws,
    SUM(CASE WHEN result = 'LOSS' THEN 1 ELSE 0 END) as losses,
    -- Calculate points: 3 per win, 1 per draw
    (SUM(CASE WHEN result = 'WIN' THEN 3 ELSE 0 END) + 
     SUM(CASE WHEN result = 'DRAW' THEN 1 ELSE 0 END)) as points
FROM player_matches
GROUP BY season_id, season_name, player_id, player_name
ORDER BY season_id, points DESC, wins DESC, player_name;

COMMENT ON VIEW season_standings IS 'Player standings by season with points (3 per win, 1 per draw), ordered by points descending';

-- ============================================================================
-- END OF VIEWS
-- ============================================================================
