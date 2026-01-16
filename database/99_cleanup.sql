-- MTG Tournament Tracker - Database Cleanup Script
-- Deletes all data in correct order to avoid foreign key constraint violations
-- WARNING: This will delete ALL data from the database!

BEGIN;

-- Step 1: Delete games (depends on matches)
DELETE FROM games;

-- Step 2: Delete matches (depends on tournaments, players, deck_archetypes)
DELETE FROM matches;

-- Step 3: Delete tournaments (depends on seasons)
DELETE FROM tournaments;

-- Step 4: Delete tournament types (no dependencies once tournaments are cleared)
DELETE FROM tournament_types;

-- Step 5: Delete deck archetypes (no dependencies)
DELETE FROM deck_archetypes;

-- Step 6: Delete players (no dependencies)
DELETE FROM players;

-- Step 7: Delete seasons (no dependencies)
DELETE FROM seasons;

-- Reset sequences to start from 1 again
ALTER SEQUENCE seasons_id_seq RESTART WITH 1;
ALTER SEQUENCE tournaments_id_seq RESTART WITH 1;
ALTER SEQUENCE tournament_types_id_seq RESTART WITH 1;
ALTER SEQUENCE players_id_seq RESTART WITH 1;
ALTER SEQUENCE deck_archetypes_id_seq RESTART WITH 1;
ALTER SEQUENCE matches_id_seq RESTART WITH 1;
ALTER SEQUENCE games_id_seq RESTART WITH 1;

COMMIT;

-- Re-enable triggers (if disabled above)
-- SET session_replication_role = 'origin';

-- Verify all tables are empty
SELECT 
    'seasons' as table_name, COUNT(*) as row_count FROM seasons
UNION ALL
SELECT 'tournaments', COUNT(*) FROM tournaments
UNION ALL
SELECT 'tournament_types', COUNT(*) FROM tournament_types
UNION ALL
SELECT 'players', COUNT(*) FROM players
UNION ALL
SELECT 'deck_archetypes', COUNT(*) FROM deck_archetypes
UNION ALL
SELECT 'matches', COUNT(*) FROM matches
UNION ALL
SELECT 'games', COUNT(*) FROM games
ORDER BY table_name;

-- Success message
\echo '✓ Database cleanup complete! All tables are empty and sequences reset.'
