-- ============================================================================
-- Sample Query: Player Matches by Tournament Type with Results
-- ============================================================================
-- Description: Get the number of matches a player played in a specific season
--              broken down by tournament type, showing wins, draws, and losses
-- 
-- Example: Charlie Davis in 2026 Q1 Standard Season
-- ============================================================================

SELECT
    p.name AS player_name,
    s.name AS season_name,
    tt.name AS tournament_type,
    COUNT(DISTINCT m.id) AS matches_played,
    COUNT(CASE 
        WHEN (m.player1_id = p.id AND mr.player1_result = 'WIN') 
          OR (m.player2_id = p.id AND mr.player2_result = 'WIN') 
        THEN 1 
    END) AS match_wins,
    COUNT(CASE 
        WHEN (m.player1_id = p.id AND mr.player1_result = 'DRAW') 
          OR (m.player2_id = p.id AND mr.player2_result = 'DRAW') 
        THEN 1 
    END) AS match_draws,
    COUNT(CASE 
        WHEN (m.player1_id = p.id AND mr.player1_result = 'LOSS') 
          OR (m.player2_id = p.id AND mr.player2_result = 'LOSS') 
        THEN 1 
    END) AS match_losses
FROM players p
INNER JOIN matches m ON (m.player1_id = p.id OR m.player2_id = p.id)
INNER JOIN tournaments t ON m.tournament_id = t.id
INNER JOIN tournament_types tt ON t.tournament_type_id = tt.id
INNER JOIN seasons s ON t.season_id = s.id
LEFT JOIN match_results mr ON mr.match_id = m.id
WHERE 
    p.name = 'Charlie Davis'
    AND s.name = '2026 Q1 Standard Season'
GROUP BY 
    p.id, p.name, s.id, s.name, tt.id, tt.name
ORDER BY 
    tt.name;
