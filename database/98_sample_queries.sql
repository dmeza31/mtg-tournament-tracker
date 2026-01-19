-- ============================================================================
-- MTG Tournament Tracking System - Sample Queries
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Example queries demonstrating how to retrieve the requested
--              statistics and analytics from the database
-- ============================================================================

-- ============================================================================
-- PLAYER STATISTICS QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 1: Number of matches won grouped by player
-- ----------------------------------------------------------------------------
SELECT 
    player_name,
    matches_won,
    total_matches,
    win_rate_percentage
FROM player_statistics
ORDER BY matches_won DESC, player_name;

-- Alternative: More detailed query with player info
SELECT 
    p.id,
    p.name,
    p.email,
    ps.matches_won,
    ps.total_matches,
    ps.win_rate_percentage,
    ps.tournaments_played
FROM player_statistics ps
JOIN players p ON ps.player_id = p.id
ORDER BY ps.matches_won DESC;

-- ----------------------------------------------------------------------------
-- Query 2: Number of matches drawn grouped by player
-- ----------------------------------------------------------------------------
SELECT 
    player_name,
    matches_drawn,
    total_matches,
    ROUND(100.0 * matches_drawn / NULLIF(total_matches, 0), 2) as draw_rate_percentage
FROM player_statistics
ORDER BY matches_drawn DESC, player_name;

-- ----------------------------------------------------------------------------
-- Query 3: Number of matches lost grouped by player
-- ----------------------------------------------------------------------------
SELECT 
    player_name,
    matches_lost,
    total_matches,
    ROUND(100.0 * matches_lost / NULLIF(total_matches, 0), 2) as loss_rate_percentage
FROM player_statistics
ORDER BY matches_lost DESC, player_name;

-- ----------------------------------------------------------------------------
-- Query 4: Complete player statistics (wins, draws, losses in one query)
-- ----------------------------------------------------------------------------
SELECT 
    player_name,
    total_matches,
    matches_won,
    matches_drawn,
    matches_lost,
    win_rate_percentage
FROM player_statistics
ORDER BY win_rate_percentage DESC, matches_won DESC;

-- ----------------------------------------------------------------------------
-- Query 5: Player statistics for a specific season
-- ----------------------------------------------------------------------------
SELECT 
    p.name as player_name,
    COUNT(*) as total_matches,
    SUM(CASE WHEN 
        (m.player1_id = p.id AND mr.player1_result = 'WIN') OR 
        (m.player2_id = p.id AND mr.player2_result = 'WIN')
        THEN 1 ELSE 0 END) as matches_won,
    SUM(CASE WHEN 
        (m.player1_id = p.id AND mr.player1_result = 'DRAW') OR 
        (m.player2_id = p.id AND mr.player2_result = 'DRAW')
        THEN 1 ELSE 0 END) as matches_drawn,
    SUM(CASE WHEN 
        (m.player1_id = p.id AND mr.player1_result = 'LOSS') OR 
        (m.player2_id = p.id AND mr.player2_result = 'LOSS')
        THEN 1 ELSE 0 END) as matches_lost
FROM players p
JOIN matches m ON p.id = m.player1_id OR p.id = m.player2_id
JOIN match_results mr ON m.id = mr.match_id
JOIN tournaments t ON m.tournament_id = t.id
JOIN seasons s ON t.season_id = s.id
WHERE s.name = '2026 Standard Season'  -- Replace with desired season
  AND m.match_status = 'COMPLETED'
GROUP BY p.id, p.name
ORDER BY matches_won DESC;

-- ============================================================================
-- DECK STATISTICS QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 6: Number of matches won grouped by deck
-- ----------------------------------------------------------------------------
SELECT 
    deck_name,
    color_identity,
    archetype_type,
    matches_won,
    total_matches,
    win_rate_percentage
FROM deck_statistics
ORDER BY matches_won DESC, deck_name;

-- ----------------------------------------------------------------------------
-- Query 7: Number of matches drawn grouped by deck
-- ----------------------------------------------------------------------------
SELECT 
    deck_name,
    color_identity,
    matches_drawn,
    total_matches,
    ROUND(100.0 * matches_drawn / NULLIF(total_matches, 0), 2) as draw_rate_percentage
FROM deck_statistics
ORDER BY matches_drawn DESC, deck_name;

-- ----------------------------------------------------------------------------
-- Query 8: Number of matches lost grouped by deck
-- ----------------------------------------------------------------------------
SELECT 
    deck_name,
    color_identity,
    matches_lost,
    total_matches,
    ROUND(100.0 * matches_lost / NULLIF(total_matches, 0), 2) as loss_rate_percentage
FROM deck_statistics
ORDER BY matches_lost DESC, deck_name;

-- ----------------------------------------------------------------------------
-- Query 9: Complete deck statistics (wins, draws, losses in one query)
-- ----------------------------------------------------------------------------
SELECT 
    deck_name,
    color_identity,
    archetype_type,
    total_matches,
    matches_won,
    matches_drawn,
    matches_lost,
    win_rate_percentage,
    unique_players
FROM deck_statistics
ORDER BY win_rate_percentage DESC, matches_won DESC;

-- ----------------------------------------------------------------------------
-- Query 10: Deck statistics by archetype type (Aggro, Control, etc.)
-- ----------------------------------------------------------------------------
SELECT 
    archetype_type,
    COUNT(*) as num_decks,
    SUM(total_matches) as total_matches,
    SUM(matches_won) as total_wins,
    ROUND(100.0 * SUM(matches_won) / NULLIF(SUM(total_matches), 0), 2) as avg_win_rate
FROM deck_statistics
GROUP BY archetype_type
ORDER BY avg_win_rate DESC;

-- ============================================================================
-- DECK MATCHUP QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 11: Win rate of specific deck X vs deck Y
-- ----------------------------------------------------------------------------
-- Example: "Mono Red Aggro" vs "Azorius Control"
SELECT 
    deck_a_name,
    deck_b_name,
    total_matches,
    deck_a_wins,
    draws,
    deck_a_losses,
    deck_a_win_rate_percentage,
    deck_b_win_rate_percentage
FROM deck_matchups
WHERE deck_a_name = 'Mono Red Aggro' 
  AND deck_b_name = 'Azorius Control';

-- Alternative: Show both directions (A vs B and B vs A)
SELECT 
    deck_a_name as deck_x,
    deck_b_name as deck_y,
    total_matches,
    deck_a_wins as deck_x_wins,
    draws,
    deck_a_losses as deck_x_losses,
    deck_a_win_rate_percentage as deck_x_win_rate
FROM deck_matchups
WHERE (deck_a_name = 'Mono Red Aggro' AND deck_b_name = 'Azorius Control')
   OR (deck_a_name = 'Azorius Control' AND deck_b_name = 'Mono Red Aggro');

-- ----------------------------------------------------------------------------
-- Query 12: All matchups for a specific deck
-- ----------------------------------------------------------------------------
-- Shows how a specific deck performs against all other decks
SELECT 
    deck_a_name as your_deck,
    deck_b_name as opponent_deck,
    total_matches,
    deck_a_wins as your_wins,
    deck_a_losses as your_losses,
    deck_a_win_rate_percentage as your_win_rate
FROM deck_matchups
WHERE deck_a_name = 'Mono Red Aggro'
ORDER BY total_matches DESC, your_win_rate DESC;

-- ----------------------------------------------------------------------------
-- Query 13: Top 10 most played matchups
-- ----------------------------------------------------------------------------
SELECT 
    deck_a_name,
    deck_b_name,
    total_matches,
    deck_a_wins,
    draws,
    deck_a_losses,
    deck_a_win_rate_percentage
FROM deck_matchups
ORDER BY total_matches DESC
LIMIT 10;

-- ----------------------------------------------------------------------------
-- Query 14: Most favorable matchups (highest win rate with minimum matches)
-- ----------------------------------------------------------------------------
-- Shows matchups where deck_a has the highest win rate
-- (Minimum 5 matches to ensure statistical significance)
SELECT 
    deck_a_name,
    deck_b_name,
    total_matches,
    deck_a_wins,
    deck_a_win_rate_percentage
FROM deck_matchups
WHERE total_matches >= 5
ORDER BY deck_a_win_rate_percentage DESC, total_matches DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- Query 15: Detailed matchup analysis with game-level data
-- ----------------------------------------------------------------------------
-- Shows detailed game results for a specific matchup
SELECT 
    mr.match_id,
    t.name as tournament_name,
    t.tournament_date,
    p1.name as player1_name,
    da1.name as player1_deck,
    p2.name as player2_name,
    da2.name as player2_deck,
    mr.player1_game_wins,
    mr.player2_game_wins,
    CASE 
        WHEN mr.match_winner_id = mr.player1_id THEN p1.name
        WHEN mr.match_winner_id = mr.player2_id THEN p2.name
        ELSE 'DRAW'
    END as match_winner
FROM match_results mr
JOIN matches m ON mr.match_id = m.id
JOIN tournaments t ON mr.tournament_id = t.id
JOIN players p1 ON mr.player1_id = p1.id
JOIN players p2 ON mr.player2_id = p2.id
JOIN deck_archetypes da1 ON mr.player1_deck_id = da1.id
JOIN deck_archetypes da2 ON mr.player2_deck_id = da2.id
WHERE da1.name = 'Mono Red Aggro' AND da2.name = 'Azorius Control'
ORDER BY t.tournament_date DESC;

-- ============================================================================
-- ADVANCED ANALYTICS QUERIES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 16: Player performance with each deck they've played
-- ----------------------------------------------------------------------------
SELECT 
    player_name,
    deck_name,
    total_matches,
    matches_won,
    matches_drawn,
    matches_lost,
    win_rate_percentage
FROM player_deck_performance
ORDER BY player_name, win_rate_percentage DESC;

-- ----------------------------------------------------------------------------
-- Query 17: Most successful player-deck combinations
-- ----------------------------------------------------------------------------
-- Shows players who have the best performance with specific decks
-- (Minimum 3 matches to filter out small samples)
SELECT 
    player_name,
    deck_name,
    total_matches,
    matches_won,
    win_rate_percentage
FROM player_deck_performance
WHERE total_matches >= 3
ORDER BY win_rate_percentage DESC, matches_won DESC
LIMIT 20;

-- ----------------------------------------------------------------------------
-- Query 18: Meta analysis - deck popularity and performance
-- ----------------------------------------------------------------------------
-- Shows which decks are most played and how well they perform
SELECT 
    ds.deck_name,
    ds.color_identity,
    ds.archetype_type,
    ds.total_matches,
    ds.win_rate_percentage,
    ds.unique_players,
    ROUND(100.0 * ds.total_matches / NULLIF(SUM(ds.total_matches) OVER(), 0), 2) as meta_percentage
FROM deck_statistics ds
ORDER BY ds.total_matches DESC;

-- ----------------------------------------------------------------------------
-- Query 19: Player consistency - players with most balanced records
-- ----------------------------------------------------------------------------
-- Finds players with good win rates and substantial match history
SELECT 
    player_name,
    total_matches,
    matches_won,
    matches_drawn,
    matches_lost,
    win_rate_percentage,
    tournaments_played,
    decks_played
FROM player_statistics
WHERE total_matches >= 10
ORDER BY win_rate_percentage DESC, total_matches DESC;

-- ----------------------------------------------------------------------------
-- Query 20: Tournament winners and top performers
-- ----------------------------------------------------------------------------
-- Identifies top performers in each tournament
WITH tournament_player_stats AS (
    SELECT 
        t.id as tournament_id,
        t.name as tournament_name,
        t.tournament_date,
        p.id as player_id,
        p.name as player_name,
        COUNT(*) as matches_played,
        SUM(CASE WHEN 
            (m.player1_id = p.id AND mr.player1_result = 'WIN') OR 
            (m.player2_id = p.id AND mr.player2_result = 'WIN')
            THEN 1 ELSE 0 END) as matches_won
    FROM tournaments t
    JOIN matches m ON t.id = m.tournament_id
    JOIN match_results mr ON m.id = mr.match_id
    JOIN players p ON p.id = m.player1_id OR p.id = m.player2_id
    WHERE m.match_status = 'COMPLETED'
    GROUP BY t.id, t.name, t.tournament_date, p.id, p.name
)
SELECT 
    tournament_name,
    tournament_date,
    player_name,
    matches_played,
    matches_won,
    RANK() OVER (PARTITION BY tournament_id ORDER BY matches_won DESC, matches_played DESC) as tournament_rank
FROM tournament_player_stats
ORDER BY tournament_date DESC, tournament_rank;

-- ============================================================================
-- FILTERING EXAMPLES
-- ============================================================================

-- ----------------------------------------------------------------------------
-- Query 21: Statistics for a specific time period
-- ----------------------------------------------------------------------------
SELECT 
    p.name as player_name,
    COUNT(*) as total_matches,
    SUM(CASE WHEN 
        (m.player1_id = p.id AND mr.player1_result = 'WIN') OR 
        (m.player2_id = p.id AND mr.player2_result = 'WIN')
        THEN 1 ELSE 0 END) as matches_won
FROM players p
JOIN matches m ON p.id = m.player1_id OR p.id = m.player2_id
JOIN match_results mr ON m.id = mr.match_id
WHERE m.match_status = 'COMPLETED'
  AND m.match_date >= '2026-01-01'
  AND m.match_date < '2026-02-01'
GROUP BY p.id, p.name
ORDER BY matches_won DESC;

-- ----------------------------------------------------------------------------
-- Query 22: Deck performance in specific format
-- ----------------------------------------------------------------------------
SELECT 
    da.name as deck_name,
    t.format,
    COUNT(*) as total_matches,
    SUM(CASE WHEN mr.player1_result = 'WIN' THEN 1 ELSE 0 END) as matches_won_as_p1,
    SUM(CASE WHEN mr.player2_result = 'WIN' THEN 1 ELSE 0 END) as matches_won_as_p2
FROM deck_archetypes da
JOIN matches m ON da.id = m.player1_deck_id OR da.id = m.player2_deck_id
JOIN match_results mr ON m.id = mr.match_id
JOIN tournaments t ON m.tournament_id = t.id
WHERE t.format = 'Standard'
  AND m.match_status = 'COMPLETED'
GROUP BY da.id, da.name, t.format
ORDER BY total_matches DESC;

-- ============================================================================
-- END OF SAMPLE QUERIES
-- ============================================================================
