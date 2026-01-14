-- ============================================================================
-- MTG Tournament Tracking System - Indexes
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Indexes optimized for common query patterns including:
--              - Player statistics (wins/draws/losses by player)
--              - Deck statistics (wins/draws/losses by deck archetype)
--              - Deck matchup analysis (Deck X vs Deck Y win rates)
--              - Tournament lookups and date-range queries
-- ============================================================================

-- ============================================================================
-- SEASONS INDEXES
-- ============================================================================
CREATE INDEX idx_seasons_dates ON seasons(start_date, end_date);

COMMENT ON INDEX idx_seasons_dates IS 'Optimize date range queries for active seasons';

-- ============================================================================
-- TOURNAMENTS INDEXES
-- ============================================================================
CREATE INDEX idx_tournaments_season ON tournaments(season_id);
CREATE INDEX idx_tournaments_date ON tournaments(tournament_date DESC);
CREATE INDEX idx_tournaments_season_date ON tournaments(season_id, tournament_date DESC);

COMMENT ON INDEX idx_tournaments_season IS 'Lookup tournaments by season';
COMMENT ON INDEX idx_tournaments_date IS 'Date-ordered tournament queries';
COMMENT ON INDEX idx_tournaments_season_date IS 'Season-specific date range queries';

-- ============================================================================
-- PLAYERS INDEXES
-- ============================================================================
CREATE INDEX idx_players_active ON players(active) WHERE active = TRUE;
CREATE INDEX idx_players_name ON players(name);

COMMENT ON INDEX idx_players_active IS 'Partial index for active players only';
COMMENT ON INDEX idx_players_name IS 'Player name lookups and sorting';

-- ============================================================================
-- DECK_ARCHETYPES INDEXES
-- ============================================================================
CREATE INDEX idx_deck_archetypes_name ON deck_archetypes(name);
CREATE INDEX idx_deck_archetypes_type ON deck_archetypes(archetype_type);

COMMENT ON INDEX idx_deck_archetypes_name IS 'Deck archetype name lookups';
COMMENT ON INDEX idx_deck_archetypes_type IS 'Filter by archetype type (Aggro, Control, etc.)';

-- ============================================================================
-- MATCHES INDEXES
-- ============================================================================

-- Tournament-based lookups
CREATE INDEX idx_matches_tournament ON matches(tournament_id, round_number);

-- Player-based lookups (for aggregating player statistics)
CREATE INDEX idx_matches_player1 ON matches(player1_id, player1_deck_id);
CREATE INDEX idx_matches_player2 ON matches(player2_id, player2_deck_id);

-- Deck matchup analysis (both directions)
CREATE INDEX idx_matches_deck_matchup ON matches(player1_deck_id, player2_deck_id);

-- Date-based queries
CREATE INDEX idx_matches_date ON matches(match_date DESC);

-- Status filtering (completed matches for statistics)
CREATE INDEX idx_matches_status ON matches(match_status) WHERE match_status = 'COMPLETED';

COMMENT ON INDEX idx_matches_tournament IS 'Tournament matches ordered by round';
COMMENT ON INDEX idx_matches_player1 IS 'Player 1 statistics and deck usage';
COMMENT ON INDEX idx_matches_player2 IS 'Player 2 statistics and deck usage';
COMMENT ON INDEX idx_matches_deck_matchup IS 'Deck archetype matchup analysis';
COMMENT ON INDEX idx_matches_date IS 'Time-series match queries';
COMMENT ON INDEX idx_matches_status IS 'Filter completed matches for statistics';

-- ============================================================================
-- GAMES INDEXES
-- ============================================================================

-- Match-based lookups (get all games in a match)
CREATE INDEX idx_games_match ON games(match_id, game_number);

-- Winner-based aggregations (player win statistics)
CREATE INDEX idx_games_winner ON games(winner_id, game_result);

-- Composite index for player game statistics
-- This enables efficient queries joining matches and games to get player performance
CREATE INDEX idx_games_match_winner_result ON games(match_id, winner_id, game_result);

COMMENT ON INDEX idx_games_match IS 'Retrieve games for a specific match';
COMMENT ON INDEX idx_games_winner IS 'Player game win statistics';
COMMENT ON INDEX idx_games_match_winner_result IS 'Efficient match-to-player-result joins';

-- ============================================================================
-- SPECIALIZED INDEXES FOR COMMON QUERY PATTERNS
-- ============================================================================

-- Index for "games won by player with specific deck" queries
-- This supports queries that join matches and games to aggregate player+deck performance
CREATE INDEX idx_games_winner_match_covering ON games(winner_id, match_id) 
    INCLUDE (game_result, game_number);

COMMENT ON INDEX idx_games_winner_match_covering IS 'Covering index for player performance queries';

-- Partial index for win-only statistics (excludes draws)
CREATE INDEX idx_games_wins_only ON games(winner_id, match_id) 
    WHERE game_result = 'WIN';

COMMENT ON INDEX idx_games_wins_only IS 'Partial index optimized for win-only queries';

-- ============================================================================
-- PERFORMANCE NOTES
-- ============================================================================
-- 
-- Query Performance Considerations:
--
-- 1. Player Statistics Queries:
--    - Use idx_games_winner and idx_matches_player1/player2 for aggregations
--    - JOIN games with matches to get deck information
--
-- 2. Deck Statistics Queries:
--    - Use idx_matches_deck_matchup combined with idx_games_match
--    - Consider creating materialized view for frequently accessed deck stats
--
-- 3. Deck Matchup Queries (Deck X vs Deck Y):
--    - Use idx_matches_deck_matchup to filter relevant matches
--    - JOIN with games to determine match winners
--    - May benefit from materialized view if matchup data is historical
--
-- 4. Large Dataset Optimizations:
--    - If tournament history spans multiple years, consider partitioning
--      matches and games tables by year or season
--    - Use BRIN indexes on match_date for very large time-series data
--    - Create materialized views for expensive aggregations and refresh
--      periodically (e.g., after each tournament)
--
-- 5. Index Maintenance:
--    - PostgreSQL auto-vacuums to maintain index health
--    - For bulk inserts, consider temporarily dropping indexes and rebuilding
--    - Monitor index usage with pg_stat_user_indexes view
--    - Use ANALYZE after bulk data loads to update statistics
--
-- ============================================================================
-- END OF INDEXES
-- ============================================================================
