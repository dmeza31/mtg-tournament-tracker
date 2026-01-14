-- ============================================================================
-- MTG Tournament Tracking System - Sample Data
-- PostgreSQL Implementation
-- ============================================================================
-- Description: Sample data for testing the database schema, views, and queries
--              Includes realistic MTG tournament scenarios with multiple
--              players, decks, and best-of-3 match results
-- ============================================================================

-- ============================================================================
-- SEASONS
-- ============================================================================
INSERT INTO seasons (name, start_date, end_date, description) VALUES
('2026 Standard Season', '2026-01-01', '2026-03-31', 'Q1 2026 Standard tournament season'),
('2026 Modern Season', '2026-04-01', '2026-06-30', 'Q2 2026 Modern tournament season');

-- ============================================================================
-- TOURNAMENTS
-- ============================================================================
INSERT INTO tournaments (season_id, name, tournament_date, location, format, description) VALUES
(1, 'January Standard Showdown', '2026-01-15', 'Local Game Store - Downtown', 'Standard', 'Weekly Standard tournament'),
(1, 'February Championship Qualifier', '2026-02-20', 'Convention Center', 'Standard', 'Regional Championship Qualifier'),
(1, 'March Season Finale', '2026-03-28', 'Local Game Store - Downtown', 'Standard', 'End of season tournament');

-- ============================================================================
-- PLAYERS
-- ============================================================================
INSERT INTO players (name, email, registration_date, active) VALUES
('Alice Johnson', 'alice.johnson@email.com', '2025-12-01', TRUE),
('Bob Smith', 'bob.smith@email.com', '2025-12-05', TRUE),
('Charlie Davis', 'charlie.davis@email.com', '2025-12-10', TRUE),
('Diana Martinez', 'diana.martinez@email.com', '2025-12-15', TRUE),
('Ethan Wilson', 'ethan.wilson@email.com', '2026-01-02', TRUE),
('Fiona Chen', 'fiona.chen@email.com', '2026-01-08', TRUE),
('George Taylor', 'george.taylor@email.com', '2026-01-12', TRUE),
('Hannah Lee', 'hannah.lee@email.com', '2026-01-20', TRUE);

-- ============================================================================
-- DECK ARCHETYPES
-- ============================================================================
INSERT INTO deck_archetypes (name, color_identity, archetype_type, description) VALUES
('Mono Red Aggro', 'R', 'Aggro', 'Fast aggressive red deck with burn spells'),
('Azorius Control', 'WU', 'Control', 'Blue-white control deck with counterspells and board wipes'),
('Golgari Midrange', 'BG', 'Midrange', 'Black-green midrange deck with efficient creatures'),
('Rakdos Sacrifice', 'BR', 'Midrange', 'Black-red deck focused on sacrifice synergies'),
('Bant Ramp', 'WUG', 'Ramp', 'Three-color ramp deck with big payoffs'),
('Dimir Aggro', 'UB', 'Aggro', 'Blue-black aggressive deck with tempo elements'),
('Selesnya Tokens', 'WG', 'Aggro', 'White-green token strategy'),
('Izzet Tempo', 'UR', 'Tempo', 'Blue-red tempo deck with cheap threats and interaction');

-- ============================================================================
-- TOURNAMENT 1: January Standard Showdown (2026-01-15)
-- ============================================================================

-- Round 1 Matches
-- Match 1: Alice (Mono Red Aggro) vs Bob (Azorius Control)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 1, 2, 1, 2, 1, '2026-01-15 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(1, 1, 1, 'WIN', 12),  -- Alice wins game 1
(1, 2, 2, 'WIN', 18),  -- Bob wins game 2
(1, 3, 1, 'WIN', 15);  -- Alice wins game 3 (Alice wins match 2-1)

-- Match 2: Charlie (Golgari Midrange) vs Diana (Rakdos Sacrifice)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 3, 4, 3, 4, 1, '2026-01-15 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(2, 1, 3, 'WIN', 20),  -- Charlie wins game 1
(2, 2, 3, 'WIN', 22);  -- Charlie wins game 2 (Charlie wins match 2-0)

-- Match 3: Ethan (Bant Ramp) vs Fiona (Dimir Aggro)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 5, 6, 5, 6, 1, '2026-01-15 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(3, 1, 6, 'WIN', 14),  -- Fiona wins game 1
(3, 2, 6, 'WIN', 16);  -- Fiona wins game 2 (Fiona wins match 2-0)

-- Match 4: George (Selesnya Tokens) vs Hannah (Izzet Tempo)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 7, 8, 7, 8, 1, '2026-01-15 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(4, 1, 7, 'WIN', 17),  -- George wins game 1
(4, 2, 8, 'WIN', 19),  -- Hannah wins game 2
(4, 3, 8, 'WIN', 21);  -- Hannah wins game 3 (Hannah wins match 2-1)

-- Round 2 Matches
-- Match 5: Alice (Mono Red Aggro) vs Charlie (Golgari Midrange) - Winners from Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 1, 3, 1, 3, 2, '2026-01-15 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(5, 1, 1, 'WIN', 13),  -- Alice wins game 1
(5, 2, 3, 'WIN', 25),  -- Charlie wins game 2
(5, 3, 3, 'WIN', 28);  -- Charlie wins game 3 (Charlie wins match 2-1)

-- Match 6: Fiona (Dimir Aggro) vs Hannah (Izzet Tempo) - Winners from Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 6, 8, 6, 8, 2, '2026-01-15 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(6, 1, 8, 'WIN', 15),  -- Hannah wins game 1
(6, 2, 8, 'WIN', 17);  -- Hannah wins game 2 (Hannah wins match 2-0)

-- Match 7: Bob (Azorius Control) vs Diana (Rakdos Sacrifice) - Losers from Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 2, 4, 2, 4, 2, '2026-01-15 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(7, 1, 2, 'WIN', 24),  -- Bob wins game 1
(7, 2, 4, 'WIN', 20),  -- Diana wins game 2
(7, 3, 2, 'WIN', 26);  -- Bob wins game 3 (Bob wins match 2-1)

-- Match 8: Ethan (Bant Ramp) vs George (Selesnya Tokens) - Losers from Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 5, 7, 5, 7, 2, '2026-01-15 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(8, 1, 5, 'WIN', 27),  -- Ethan wins game 1
(8, 2, 7, 'WIN', 23),  -- George wins game 2
(8, 3, 5, 'WIN', 29);  -- Ethan wins game 3 (Ethan wins match 2-1)

-- Round 3 - Finals
-- Match 9: Charlie (Golgari Midrange) vs Hannah (Izzet Tempo)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (1, 3, 8, 3, 8, 3, '2026-01-15 13:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(9, 1, 3, 'WIN', 21),  -- Charlie wins game 1
(9, 2, 3, 'WIN', 24);  -- Charlie wins game 2 (Charlie wins match 2-0 and tournament)

-- ============================================================================
-- TOURNAMENT 2: February Championship Qualifier (2026-02-20)
-- ============================================================================

-- Round 1 Matches
-- Match 10: Alice (Mono Red Aggro) vs Diana (Golgari Midrange)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 1, 4, 1, 3, 1, '2026-02-20 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(10, 1, 1, 'WIN', 11),  -- Alice wins game 1
(10, 2, 4, 'WIN', 23),  -- Diana wins game 2
(10, 3, 1, 'WIN', 14);  -- Alice wins game 3 (Alice wins match 2-1)

-- Match 11: Bob (Azorius Control) vs Fiona (Dimir Aggro)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 2, 6, 2, 6, 1, '2026-02-20 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(11, 1, 2, 'WIN', 22),  -- Bob wins game 1
(11, 2, 6, 'WIN', 16),  -- Fiona wins game 2
(11, 3, 2, 'WIN', 25);  -- Bob wins game 3 (Bob wins match 2-1)

-- Match 12: Charlie (Golgari Midrange) vs Ethan (Rakdos Sacrifice)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 3, 5, 3, 4, 1, '2026-02-20 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(12, 1, 5, 'WIN', 19),  -- Ethan wins game 1
(12, 2, 3, 'WIN', 26),  -- Charlie wins game 2
(12, 3, 3, 'WIN', 27);  -- Charlie wins game 3 (Charlie wins match 2-1)

-- Match 13: George (Selesnya Tokens) vs Hannah (Izzet Tempo)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 7, 8, 7, 8, 1, '2026-02-20 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(13, 1, 8, 'WIN', 18),  -- Hannah wins game 1
(13, 2, 7, 'WIN', 20),  -- George wins game 2
(13, 3, 8, 'WIN', 22);  -- Hannah wins game 3 (Hannah wins match 2-1)

-- Round 2 Matches
-- Match 14: Alice (Mono Red Aggro) vs Bob (Azorius Control) - Rematch!
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 1, 2, 1, 2, 2, '2026-02-20 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(14, 1, 2, 'WIN', 26),  -- Bob wins game 1
(14, 2, 1, 'WIN', 13),  -- Alice wins game 2
(14, 3, 2, 'WIN', 28);  -- Bob wins game 3 (Bob wins match 2-1)

-- Match 15: Charlie (Golgari Midrange) vs Hannah (Izzet Tempo)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 3, 8, 3, 8, 2, '2026-02-20 11:30:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(15, 1, 8, 'WIN', 17),  -- Hannah wins game 1
(15, 2, 3, 'WIN', 25),  -- Charlie wins game 2
(15, 3, 8, 'WIN', 19);  -- Hannah wins game 3 (Hannah wins match 2-1)

-- Finals
-- Match 16: Bob (Azorius Control) vs Hannah (Izzet Tempo)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (2, 2, 8, 2, 8, 3, '2026-02-20 13:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(16, 1, 8, 'WIN', 20),  -- Hannah wins game 1
(16, 2, 2, 'WIN', 27),  -- Bob wins game 2
(16, 3, 8, 'WIN', 23);  -- Hannah wins game 3 (Hannah wins match 2-1 and tournament)

-- ============================================================================
-- ADDITIONAL MATCHES: To create more data for deck matchup analysis
-- ============================================================================

-- Tournament 3 Matches
-- Match 17: Mono Red Aggro vs Azorius Control (3rd instance)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (3, 1, 2, 1, 2, 1, '2026-03-28 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(17, 1, 1, 'WIN', 14),  -- Alice wins game 1
(17, 2, 1, 'WIN', 12);  -- Alice wins game 2 (Alice wins match 2-0)

-- Match 18: Golgari Midrange vs Izzet Tempo (3rd instance)
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (3, 3, 8, 3, 8, 1, '2026-03-28 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(18, 1, 3, 'WIN', 22),  -- Charlie wins game 1
(18, 2, 8, 'WIN', 18),  -- Hannah wins game 2
(18, 3, 3, 'WIN', 24);  -- Charlie wins game 3 (Charlie wins match 2-1)

-- Match 19: Dimir Aggro vs Selesnya Tokens
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (3, 6, 7, 6, 7, 1, '2026-03-28 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(19, 1, 6, 'WIN', 15),  -- Fiona wins game 1
(19, 2, 6, 'WIN', 17);  -- Fiona wins game 2 (Fiona wins match 2-0)

-- Match 20: Rakdos Sacrifice vs Bant Ramp
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (3, 4, 5, 4, 5, 1, '2026-03-28 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(20, 1, 4, 'WIN', 21),  -- Diana wins game 1
(20, 2, 5, 'WIN', 26),  -- Ethan wins game 2
(20, 3, 4, 'WIN', 23);  -- Diana wins game 3 (Diana wins match 2-1)

-- ============================================================================
-- DATA VERIFICATION
-- ============================================================================

-- You can verify the data with these queries:
-- SELECT * FROM seasons;
-- SELECT * FROM tournaments;
-- SELECT * FROM players;
-- SELECT * FROM deck_archetypes;
-- SELECT * FROM matches ORDER BY match_date, id;
-- SELECT * FROM games ORDER BY match_id, game_number;

-- ============================================================================
-- END OF SAMPLE DATA
-- ============================================================================
