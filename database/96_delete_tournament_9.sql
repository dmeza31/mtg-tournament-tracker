-- ============================================================================
-- Delete Tournament ID 9 and All Related Data
-- ============================================================================
-- Description: Removes tournament with ID 9 including all associated matches
--              and games. Cascading deletes are handled by foreign key 
--              constraints (ON DELETE CASCADE).
-- ============================================================================

-- Start transaction for safety
BEGIN;

-- Display tournament information before deletion
SELECT 
    t.id AS tournament_id,
    t.name AS tournament_name,
    t.tournament_date,
    t.location,
    t.format,
    s.name AS season_name,
    tt.name AS tournament_type,
    COUNT(DISTINCT m.id) AS total_matches,
    COUNT(DISTINCT g.id) AS total_games
FROM tournaments t
LEFT JOIN seasons s ON t.season_id = s.id
LEFT JOIN tournament_types tt ON t.tournament_type_id = tt.id
LEFT JOIN matches m ON m.tournament_id = t.id
LEFT JOIN games g ON g.match_id = m.id
WHERE t.id = 9
GROUP BY t.id, t.name, t.tournament_date, t.location, t.format, s.name, tt.name;

-- Verify what will be deleted
\echo '\n--- Data to be deleted ---'
SELECT 
    'Matches to delete: ' || COUNT(*) AS info
FROM matches 
WHERE tournament_id = 9;

SELECT 
    'Games to delete: ' || COUNT(*) AS info
FROM games g
INNER JOIN matches m ON g.match_id = m.id
WHERE m.tournament_id = 9;

-- Delete tournament (matches and games will cascade automatically)
-- Due to foreign key constraints:
--   - matches(tournament_id) ON DELETE CASCADE
--   - games(match_id) ON DELETE CASCADE
DELETE FROM tournaments WHERE id = 9;

-- Verify deletion
\echo '\n--- Verification after deletion ---'
SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'Tournament 9 successfully deleted'
        ELSE 'ERROR: Tournament 9 still exists'
    END AS status
FROM tournaments 
WHERE id = 9;

SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'All related matches successfully deleted'
        ELSE 'ERROR: ' || COUNT(*) || ' matches still exist'
    END AS status
FROM matches 
WHERE tournament_id = 9;

SELECT 
    CASE 
        WHEN COUNT(*) = 0 THEN 'All related games successfully deleted'
        ELSE 'ERROR: ' || COUNT(*) || ' games still exist'
    END AS status
FROM games g
INNER JOIN matches m ON g.match_id = m.id
WHERE m.tournament_id = 9;

-- Commit the transaction
-- IMPORTANT: Review the output above before committing!
-- If everything looks correct, uncomment the COMMIT line below
--COMMIT;

-- If you want to rollback instead, uncomment the line below
-- ROLLBACK;

\echo '\n--- Transaction Status ---'
\echo 'Transaction is currently OPEN. Review the output above.'
\echo 'To commit the changes, run: COMMIT;'
\echo 'To rollback the changes, run: ROLLBACK;'
