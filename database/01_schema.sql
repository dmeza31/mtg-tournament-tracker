-- ============================================================================
-- MTG Tournament Tracking System - Database Schema
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Core schema for tracking Magic the Gathering tournament
--              matches, including best-of-3 game results, player performance,
--              and deck archetype statistics across tournament seasons.
-- ============================================================================

-- Drop existing tables if they exist (in reverse dependency order)
DROP TABLE IF EXISTS games CASCADE;
DROP TABLE IF EXISTS matches CASCADE;
DROP TABLE IF EXISTS deck_archetypes CASCADE;
DROP TABLE IF EXISTS players CASCADE;
DROP TABLE IF EXISTS tournaments CASCADE;
DROP TABLE IF EXISTS tournament_types CASCADE;
DROP TABLE IF EXISTS seasons CASCADE;

-- ============================================================================
-- TOURNAMENT TYPES TABLE
-- ============================================================================
-- Stores tournament type definitions and associated points for wins/draws
CREATE TABLE tournament_types (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    points_win INTEGER NOT NULL,
    points_draw INTEGER NOT NULL,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,

    CONSTRAINT valid_points CHECK (points_win >= 0 AND points_draw >= 0)
);

COMMENT ON TABLE tournament_types IS 'Configurable tournament types with point values per result';
COMMENT ON COLUMN tournament_types.name IS 'Unique tournament type name';
COMMENT ON COLUMN tournament_types.points_win IS 'Points awarded for a match win';
COMMENT ON COLUMN tournament_types.points_draw IS 'Points awarded for a match draw';

-- Seed default tournament types (names must stay unique)
INSERT INTO tournament_types (name, points_win, points_draw, description) VALUES
('Nationals', 12, 4, 'National-level championship events'),
('Special Event', 7, 3, 'Large regional or special events'),
('LGS Tournament', 5, 2, 'Default local game store events'),
('Online Tournament', 3, 0, 'Online or casual events');

-- ============================================================================
-- SEASONS TABLE
-- ============================================================================
-- Stores tournament season information (e.g., "2026 Standard Season")
CREATE TABLE seasons (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    start_date DATE NOT NULL,
    end_date DATE,
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Ensure end_date is after start_date
    CONSTRAINT valid_season_dates CHECK (end_date IS NULL OR end_date >= start_date)
);

COMMENT ON TABLE seasons IS 'Tournament seasons grouping multiple tournaments';
COMMENT ON COLUMN seasons.name IS 'Season name, e.g., "2026 Standard Season"';

-- ============================================================================
-- TOURNAMENTS TABLE
-- ============================================================================
-- Stores individual tournament information within a season
CREATE TABLE tournaments (
    id SERIAL PRIMARY KEY,
    season_id INTEGER NOT NULL REFERENCES seasons(id) ON DELETE CASCADE,
    tournament_type_id INTEGER NOT NULL REFERENCES tournament_types(id) ON DELETE RESTRICT,
    name VARCHAR(150) NOT NULL,
    tournament_date DATE NOT NULL,
    location VARCHAR(200),
    format VARCHAR(50), -- e.g., "Standard", "Modern", "Pioneer"
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP--,
    
    -- Prevent future tournament dates
    --CONSTRAINT valid_tournament_date CHECK (tournament_date <= CURRENT_DATE)
);

COMMENT ON TABLE tournaments IS 'Individual tournaments within a season';
COMMENT ON COLUMN tournaments.format IS 'MTG format: Standard, Modern, Pioneer, etc.';

-- ============================================================================
-- PLAYERS TABLE
-- ============================================================================
-- Stores player information
CREATE TABLE players (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL,
    email VARCHAR(150) UNIQUE,
    registration_date DATE NOT NULL DEFAULT CURRENT_DATE,
    active BOOLEAN NOT NULL DEFAULT TRUE,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE players IS 'Players participating in tournaments';
COMMENT ON COLUMN players.active IS 'Whether the player is currently active';

-- ============================================================================
-- DECK_ARCHETYPES TABLE
-- ============================================================================
-- Stores deck archetype definitions (normalized for consistency)
CREATE TABLE deck_archetypes (
    id SERIAL PRIMARY KEY,
    name VARCHAR(100) NOT NULL UNIQUE,
    color_identity VARCHAR(10), -- e.g., "R", "UW", "WUBRG"
    archetype_type VARCHAR(50), -- e.g., "Aggro", "Control", "Midrange", "Combo"
    description TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP
);

COMMENT ON TABLE deck_archetypes IS 'Deck archetypes (e.g., "Mono Red Aggro", "Azorius Control")';
COMMENT ON COLUMN deck_archetypes.color_identity IS 'WUBRG color combination';
COMMENT ON COLUMN deck_archetypes.archetype_type IS 'Strategy type: Aggro, Control, Midrange, Combo';

-- ============================================================================
-- MATCHES TABLE
-- ============================================================================
-- Stores match-level information (best-of-3 matches between two players)
CREATE TABLE matches (
    id SERIAL PRIMARY KEY,
    tournament_id INTEGER NOT NULL REFERENCES tournaments(id) ON DELETE CASCADE,
    player1_id INTEGER NOT NULL REFERENCES players(id) ON DELETE RESTRICT,
    player2_id INTEGER NOT NULL REFERENCES players(id) ON DELETE RESTRICT,
    player1_deck_id INTEGER NOT NULL REFERENCES deck_archetypes(id) ON DELETE RESTRICT,
    player2_deck_id INTEGER NOT NULL REFERENCES deck_archetypes(id) ON DELETE RESTRICT,
    round_number INTEGER, -- Tournament round (e.g., Round 1, Round 2, Finals)
    match_date TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    match_status VARCHAR(20) NOT NULL DEFAULT 'COMPLETED',
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    updated_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT different_players CHECK (player1_id != player2_id),
    CONSTRAINT valid_match_status CHECK (match_status IN ('IN_PROGRESS', 'COMPLETED', 'CANCELLED')),
    CONSTRAINT valid_round_number CHECK (round_number IS NULL OR round_number > 0)
);

COMMENT ON TABLE matches IS 'Match-level information (best-of-3 between two players)';
COMMENT ON COLUMN matches.round_number IS 'Tournament round number (Swiss/Elimination)';
COMMENT ON COLUMN matches.match_status IS 'Match status: IN_PROGRESS, COMPLETED, CANCELLED';

-- ============================================================================
-- GAMES TABLE
-- ============================================================================
-- Stores individual game results within a match (best-of-3)
CREATE TABLE games (
    id SERIAL PRIMARY KEY,
    match_id INTEGER NOT NULL REFERENCES matches(id) ON DELETE CASCADE,
    game_number INTEGER NOT NULL,
    winner_id INTEGER NOT NULL REFERENCES players(id) ON DELETE RESTRICT,
    game_result VARCHAR(10) NOT NULL,
    duration_minutes INTEGER,
    notes TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT CURRENT_TIMESTAMP,
    
    -- Constraints
    CONSTRAINT valid_game_number CHECK (game_number BETWEEN 1 AND 3),
    CONSTRAINT valid_game_result CHECK (game_result IN ('WIN', 'DRAW')),
    CONSTRAINT valid_duration CHECK (duration_minutes IS NULL OR duration_minutes > 0),
    
    -- Unique constraint: one record per game number in a match
    CONSTRAINT unique_game_per_match UNIQUE (match_id, game_number)
);

COMMENT ON TABLE games IS 'Individual game results within best-of-3 matches';
COMMENT ON COLUMN games.game_number IS 'Game number within the match (1, 2, or 3)';
COMMENT ON COLUMN games.game_result IS 'WIN (winner_id won) or DRAW (tied game)';
COMMENT ON COLUMN games.winner_id IS 'Player who won this game (or either player if DRAW)';

-- ============================================================================
-- HELPER FUNCTION: Update timestamp on row modification
-- ============================================================================
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = CURRENT_TIMESTAMP;
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

-- ============================================================================
-- TRIGGERS: Auto-update updated_at columns
-- ============================================================================
CREATE TRIGGER update_seasons_updated_at
    BEFORE UPDATE ON seasons
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tournament_types_updated_at
    BEFORE UPDATE ON tournament_types
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_tournaments_updated_at
    BEFORE UPDATE ON tournaments
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_players_updated_at
    BEFORE UPDATE ON players
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_deck_archetypes_updated_at
    BEFORE UPDATE ON deck_archetypes
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

CREATE TRIGGER update_matches_updated_at
    BEFORE UPDATE ON matches
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- END OF SCHEMA
-- ============================================================================
