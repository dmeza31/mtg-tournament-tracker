-- ============================================================================
-- MTG Tournament Tracking System - Season Standings View
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Player standings by season with points system
--              - 3 points per win
--              - 1 point per draw
--              - Ordered by points descending
-- ============================================================================

-- ============================================================================
-- VIEW: season_standings
-- ============================================================================
-- Player standings by season with points per tournament type (defaults applied)
DROP VIEW IF EXISTS season_standings CASCADE;

CREATE VIEW season_standings AS
WITH player_matches AS (
    -- Player 1 perspective
    SELECT 
        t.season_id,
        s.name as season_name,
        mr.player1_id as player_id,
        p.name as player_name,
        mr.player1_result as result,
        COALESCE(tt.points_win, 3) as points_win,
        COALESCE(tt.points_draw, 1) as points_draw
    FROM match_results mr
    JOIN matches m ON mr.match_id = m.id
    JOIN tournaments t ON mr.tournament_id = t.id
    LEFT JOIN tournament_types tt ON t.tournament_type_id = tt.id
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
        mr.player2_result as result,
        COALESCE(tt.points_win, 3) as points_win,
        COALESCE(tt.points_draw, 1) as points_draw
    FROM match_results mr
    JOIN matches m ON mr.match_id = m.id
    JOIN tournaments t ON mr.tournament_id = t.id
    LEFT JOIN tournament_types tt ON t.tournament_type_id = tt.id
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
    -- Calculate points using tournament type configuration
    (SUM(CASE WHEN result = 'WIN' THEN points_win ELSE 0 END) + 
     SUM(CASE WHEN result = 'DRAW' THEN points_draw ELSE 0 END)) as points
FROM player_matches
GROUP BY season_id, season_name, player_id, player_name
ORDER BY season_id, points DESC, wins DESC, player_name;

COMMENT ON VIEW season_standings IS 'Player standings by season with tournament-type points (win/draw), ordered by points descending';

-- ============================================================================
-- END OF VIEW
-- ============================================================================
