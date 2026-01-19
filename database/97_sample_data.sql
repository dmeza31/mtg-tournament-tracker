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
('2026 Q1 Standard Season', '2026-01-01', '2026-03-31', 'Q1 2026 Standard tournament season'),
('2026 Q2 Modern Season', '2026-04-01', '2026-06-30', 'Q2 2026 Modern tournament season'),
('2026 Q3 Pioneer Season', '2026-07-01', '2026-09-30', 'Q3 2026 Pioneer tournament season'),
('2026 Q4 Legacy Season', '2026-10-01', '2026-12-31', 'Q4 2026 Legacy tournament season');

-- ============================================================================
-- TOURNAMENTS
-- ============================================================================
-- Season 1 Tournaments (Q1 - Standard)
INSERT INTO tournaments (season_id, tournament_type_id, name, tournament_date, location, format, description) VALUES
(1, 3, 'January Standard Showdown', '2026-01-15', 'Local Game Store - Downtown', 'Standard', 'Weekly Standard tournament'),
(1, 2, 'February Championship Qualifier', '2026-02-20', 'Convention Center', 'Standard', 'Regional Championship Qualifier'),
(1, 2, 'March Season Finale', '2026-03-28', 'Local Game Store - Downtown', 'Standard', 'End of season tournament');

-- Season 2 Tournaments (Q2 - Modern)
INSERT INTO tournaments (season_id, tournament_type_id, name, tournament_date, location, format, description) VALUES
(2, 3, 'April Modern Masters', '2026-04-12', 'Game Haven', 'Modern', 'Modern format tournament'),
(2, 2, 'May Modern Mayhem', '2026-05-17', 'Convention Center', 'Modern', 'Large Modern event'),
(2, 2, 'June Modern Championship', '2026-06-21', 'Local Game Store - Downtown', 'Modern', 'Season championship');

-- Season 3 Tournaments (Q3 - Pioneer)
INSERT INTO tournaments (season_id, tournament_type_id, name, tournament_date, location, format, description) VALUES
(3, 3, 'July Pioneer Open', '2026-07-10', 'Game Haven', 'Pioneer', 'Pioneer format open tournament'),
(3, 2, 'August Pioneer Challenge', '2026-08-14', 'Convention Center', 'Pioneer', 'Pioneer competitive event'),
(3, 2, 'September Pioneer Finals', '2026-09-25', 'Local Game Store - Downtown', 'Pioneer', 'Season finale');

-- Season 4 Tournaments (Q4 - Legacy)
INSERT INTO tournaments (season_id, tournament_type_id, name, tournament_date, location, format, description) VALUES
(4, 3, 'October Legacy Legends', '2026-10-09', 'Game Haven', 'Legacy', 'Legacy format tournament'),
(4, 2, 'November Legacy Showdown', '2026-11-20', 'Convention Center', 'Legacy', 'Premier Legacy event'),
(4, 1, 'December Year-End Championship', '2026-12-19', 'Convention Center', 'Legacy', 'Annual championship finale');

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
(2, 2, 3, 'DRAW', 22);  -- Draw in game 2 (Charlie wins match 1-0-1)

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
(11, 2, 2, 'DRAW', 16),  -- Draw in game 2
(11, 3, 2, 'WIN', 25);  -- Bob wins game 3 (Bob wins match 2-0-1)

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
(19, 2, 7, 'DRAW', 17);  -- Draw in game 2 (Fiona wins match 1-0-1)

-- Match 20: Rakdos Sacrifice vs Bant Ramp
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (3, 4, 5, 4, 5, 1, '2026-03-28 10:00:00', 'COMPLETED');

INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(20, 1, 4, 'WIN', 21),  -- Diana wins game 1
(20, 2, 5, 'WIN', 26),  -- Ethan wins game 2
(20, 3, 4, 'WIN', 23);  -- Diana wins game 3 (Diana wins match 2-1)

-- ============================================================================
-- SEASON 2 - Q2 MODERN SEASON
-- ============================================================================

-- TOURNAMENT 4: April Modern Masters (2026-04-12)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 1, 3, 1, 3, 1, '2026-04-12 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(21, 1, 1, 'WIN', 10), (21, 2, 3, 'WIN', 22), (21, 3, 1, 'WIN', 13);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 2, 4, 2, 4, 1, '2026-04-12 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(22, 1, 2, 'DRAW', 24), (22, 2, 2, 'WIN', 26);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 5, 7, 5, 7, 1, '2026-04-12 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(23, 1, 7, 'WIN', 18), (23, 2, 5, 'WIN', 25), (23, 3, 7, 'WIN', 20);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 6, 8, 6, 8, 1, '2026-04-12 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(24, 1, 8, 'WIN', 16), (24, 2, 6, 'WIN', 14), (24, 3, 8, 'WIN', 17);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 1, 2, 1, 2, 2, '2026-04-12 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(25, 1, 2, 'WIN', 27), (25, 2, 1, 'WIN', 11), (25, 3, 2, 'WIN', 29);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 7, 8, 7, 8, 2, '2026-04-12 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(26, 1, 8, 'WIN', 19), (26, 2, 8, 'WIN', 20);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (4, 2, 8, 2, 8, 3, '2026-04-12 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(27, 1, 2, 'WIN', 25), (27, 2, 8, 'WIN', 21), (27, 3, 2, 'WIN', 28);

-- TOURNAMENT 5: May Modern Mayhem (2026-05-17)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 1, 4, 1, 4, 1, '2026-05-17 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(28, 1, 1, 'WIN', 12), (28, 2, 1, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 2, 3, 2, 3, 1, '2026-05-17 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(29, 1, 3, 'WIN', 23), (29, 2, 2, 'WIN', 26), (29, 3, 3, 'WIN', 25);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 5, 6, 5, 6, 1, '2026-05-17 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(30, 1, 6, 'WIN', 15), (30, 2, 5, 'WIN', 27), (30, 3, 6, 'WIN', 16);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 7, 8, 7, 8, 1, '2026-05-17 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(31, 1, 8, 'WIN', 18), (31, 2, 7, 'WIN', 21), (31, 3, 8, 'WIN', 19);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 1, 3, 1, 3, 2, '2026-05-17 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(32, 1, 3, 'WIN', 24), (32, 2, 1, 'WIN', 13), (32, 3, 3, 'WIN', 26);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 6, 8, 6, 8, 2, '2026-05-17 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(33, 1, 8, 'WIN', 17), (33, 2, 8, 'WIN', 18);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (5, 3, 8, 3, 8, 3, '2026-05-17 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(34, 1, 8, 'WIN', 20), (34, 2, 3, 'WIN', 25), (34, 3, 8, 'WIN', 22);

-- TOURNAMENT 6: June Modern Championship (2026-06-21)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 1, 5, 1, 5, 1, '2026-06-21 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(35, 1, 1, 'WIN', 11), (35, 2, 5, 'WIN', 28), (35, 3, 1, 'WIN', 13);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 2, 6, 2, 6, 1, '2026-06-21 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(36, 1, 2, 'WIN', 26), (36, 2, 2, 'WIN', 27);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 3, 7, 3, 7, 1, '2026-06-21 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(37, 1, 3, 'WIN', 22), (37, 2, 7, 'WIN', 19), (37, 3, 3, 'WIN', 24);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 4, 8, 4, 8, 1, '2026-06-21 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(38, 1, 8, 'WIN', 17), (38, 2, 4, 'WIN', 21), (38, 3, 8, 'WIN', 18);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 1, 2, 1, 2, 2, '2026-06-21 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(39, 1, 1, 'WIN', 12), (39, 2, 2, 'WIN', 28), (39, 3, 1, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 3, 8, 3, 8, 2, '2026-06-21 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(40, 1, 3, 'WIN', 23), (40, 2, 3, 'WIN', 24);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (6, 1, 3, 1, 3, 3, '2026-06-21 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(41, 1, 3, 'WIN', 25), (41, 2, 1, 'WIN', 12), (41, 3, 3, 'WIN', 27);

-- ============================================================================
-- SEASON 3 - Q3 PIONEER SEASON
-- ============================================================================

-- TOURNAMENT 7: July Pioneer Open (2026-07-10)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 1, 6, 1, 6, 1, '2026-07-10 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(42, 1, 6, 'WIN', 15), (42, 2, 1, 'WIN', 11), (42, 3, 6, 'WIN', 16);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 2, 7, 2, 7, 1, '2026-07-10 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(43, 1, 2, 'WIN', 25), (43, 2, 7, 'WIN', 20), (43, 3, 2, 'WIN', 27);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 3, 8, 3, 8, 1, '2026-07-10 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(44, 1, 8, 'WIN', 18), (44, 2, 3, 'WIN', 24), (44, 3, 8, 'WIN', 19);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 4, 5, 4, 5, 1, '2026-07-10 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(45, 1, 4, 'WIN', 22), (45, 2, 5, 'WIN', 29), (45, 3, 4, 'WIN', 23);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 6, 2, 6, 2, 2, '2026-07-10 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(46, 1, 2, 'WIN', 26), (46, 2, 6, 'WIN', 14), (46, 3, 2, 'WIN', 28);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 8, 4, 8, 4, 2, '2026-07-10 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(47, 1, 8, 'WIN', 19), (47, 2, 8, 'WIN', 20);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (7, 2, 8, 2, 8, 3, '2026-07-10 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(48, 1, 8, 'WIN', 21), (48, 2, 2, 'WIN', 27), (48, 3, 8, 'WIN', 22);

-- TOURNAMENT 8: August Pioneer Challenge (2026-08-14)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 1, 7, 1, 7, 1, '2026-08-14 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(49, 1, 1, 'WIN', 10), (49, 2, 7, 'WIN', 19), (49, 3, 1, 'WIN', 12);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 2, 8, 2, 8, 1, '2026-08-14 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(50, 1, 8, 'WIN', 18), (50, 2, 2, 'WIN', 26), (50, 3, 8, 'WIN', 20);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 3, 4, 3, 4, 1, '2026-08-14 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(51, 1, 3, 'WIN', 23), (51, 2, 3, 'WIN', 24);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 5, 6, 5, 6, 1, '2026-08-14 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(52, 1, 6, 'WIN', 14), (52, 2, 5, 'WIN', 28), (52, 3, 6, 'WIN', 15);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 1, 8, 1, 8, 2, '2026-08-14 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(53, 1, 1, 'WIN', 11), (53, 2, 8, 'WIN', 19), (53, 3, 8, 'WIN', 21);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 3, 6, 3, 6, 2, '2026-08-14 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(54, 1, 3, 'WIN', 25), (54, 2, 6, 'WIN', 16), (54, 3, 3, 'WIN', 26);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (8, 8, 3, 8, 3, 3, '2026-08-14 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(55, 1, 3, 'WIN', 24), (55, 2, 8, 'WIN', 20), (55, 3, 3, 'WIN', 27);

-- TOURNAMENT 9: September Pioneer Finals (2026-09-25)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 1, 8, 1, 8, 1, '2026-09-25 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(56, 1, 8, 'WIN', 18), (56, 2, 1, 'WIN', 12), (56, 3, 8, 'WIN', 19);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 2, 3, 2, 3, 1, '2026-09-25 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(57, 1, 3, 'WIN', 23), (57, 2, 2, 'WIN', 27), (57, 3, 3, 'WIN', 25);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 4, 5, 4, 5, 1, '2026-09-25 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(58, 1, 4, 'WIN', 21), (58, 2, 4, 'WIN', 22);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 6, 7, 6, 7, 1, '2026-09-25 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(59, 1, 6, 'WIN', 15), (59, 2, 7, 'WIN', 20), (59, 3, 6, 'WIN', 16);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 8, 3, 8, 3, 2, '2026-09-25 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(60, 1, 3, 'WIN', 24), (60, 2, 8, 'WIN', 19), (60, 3, 3, 'WIN', 26);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 4, 6, 4, 6, 2, '2026-09-25 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(61, 1, 6, 'WIN', 14), (61, 2, 4, 'WIN', 21), (61, 3, 6, 'WIN', 15);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (9, 3, 6, 3, 6, 3, '2026-09-25 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(62, 1, 6, 'WIN', 16), (62, 2, 3, 'WIN', 25), (62, 3, 3, 'WIN', 27);

-- ============================================================================
-- SEASON 4 - Q4 LEGACY SEASON
-- ============================================================================

-- TOURNAMENT 10: October Legacy Legends (2026-10-09)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 1, 2, 1, 2, 1, '2026-10-09 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(63, 1, 1, 'WIN', 13), (63, 2, 2, 'WIN', 26), (63, 3, 1, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 3, 4, 3, 4, 1, '2026-10-09 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(64, 1, 3, 'WIN', 22), (64, 2, 4, 'WIN', 20), (64, 3, 3, 'WIN', 24);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 5, 6, 5, 6, 1, '2026-10-09 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(65, 1, 6, 'WIN', 15), (65, 2, 6, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 7, 8, 7, 8, 1, '2026-10-09 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(66, 1, 8, 'WIN', 17), (66, 2, 7, 'WIN', 19), (66, 3, 8, 'WIN', 18);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 1, 3, 1, 3, 2, '2026-10-09 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(67, 1, 3, 'WIN', 23), (67, 2, 1, 'WIN', 12), (67, 3, 3, 'WIN', 25);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 6, 8, 6, 8, 2, '2026-10-09 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(68, 1, 8, 'WIN', 18), (68, 2, 6, 'WIN', 15), (68, 3, 8, 'WIN', 19);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (10, 3, 8, 3, 8, 3, '2026-10-09 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(69, 1, 8, 'WIN', 20), (69, 2, 3, 'WIN', 24), (69, 3, 8, 'WIN', 21);

-- TOURNAMENT 11: November Legacy Showdown (2026-11-20)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 1, 3, 1, 3, 1, '2026-11-20 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(70, 1, 1, 'WIN', 11), (70, 2, 3, 'WIN', 24), (70, 3, 1, 'WIN', 13);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 2, 4, 2, 4, 1, '2026-11-20 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(71, 1, 2, 'WIN', 25), (71, 2, 4, 'WIN', 22), (71, 3, 2, 'WIN', 27);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 5, 7, 5, 7, 1, '2026-11-20 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(72, 1, 7, 'WIN', 18), (72, 2, 5, 'WIN', 28), (72, 3, 7, 'WIN', 20);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 6, 8, 6, 8, 1, '2026-11-20 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(73, 1, 8, 'WIN', 17), (73, 2, 8, 'WIN', 18);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 1, 2, 1, 2, 2, '2026-11-20 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(74, 1, 2, 'WIN', 26), (74, 2, 1, 'WIN', 12), (74, 3, 2, 'WIN', 28);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 7, 8, 7, 8, 2, '2026-11-20 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(75, 1, 8, 'WIN', 19), (75, 2, 7, 'WIN', 21), (75, 3, 8, 'WIN', 20);

-- Finals
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (11, 2, 8, 2, 8, 3, '2026-11-20 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(76, 1, 8, 'WIN', 21), (76, 2, 2, 'WIN', 27), (76, 3, 8, 'WIN', 22);

-- TOURNAMENT 12: December Year-End Championship (2026-12-19)
-- Round 1
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 1, 4, 1, 4, 1, '2026-12-19 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(77, 1, 1, 'WIN', 12), (77, 2, 4, 'WIN', 21), (77, 3, 1, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 2, 5, 2, 5, 1, '2026-12-19 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(78, 1, 2, 'WIN', 26), (78, 2, 2, 'WIN', 27);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 3, 6, 3, 6, 1, '2026-12-19 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(79, 1, 3, 'WIN', 23), (79, 2, 6, 'WIN', 15), (79, 3, 3, 'WIN', 25);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 7, 8, 7, 8, 1, '2026-12-19 10:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(80, 1, 8, 'WIN', 18), (80, 2, 7, 'WIN', 20), (80, 3, 8, 'WIN', 19);

-- Round 2
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 1, 2, 1, 2, 2, '2026-12-19 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(81, 1, 1, 'WIN', 13), (81, 2, 2, 'WIN', 28), (81, 3, 1, 'WIN', 14);

INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 3, 8, 3, 8, 2, '2026-12-19 11:30:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(82, 1, 3, 'WIN', 24), (82, 2, 8, 'WIN', 19), (82, 3, 3, 'WIN', 26);

-- Finals - Year-End Championship Winner!
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number, match_date, match_status)
VALUES (12, 1, 3, 1, 3, 3, '2026-12-19 13:00:00', 'COMPLETED');
INSERT INTO games (match_id, game_number, winner_id, game_result, duration_minutes) VALUES
(83, 1, 3, 'WIN', 25), (83, 2, 1, 'WIN', 12), (83, 3, 3, 'WIN', 28);

-- ============================================================================
-- DATA VERIFICATION
-- ============================================================================

-- You can verify the data with these queries:
-- SELECT * FROM seasons ORDER BY start_date;
-- SELECT * FROM tournaments ORDER BY tournament_date;
-- SELECT * FROM players;
-- SELECT * FROM deck_archetypes;
-- SELECT COUNT(*) as total_matches FROM matches;
-- SELECT COUNT(*) as total_games FROM games;
-- SELECT * FROM season_standings ORDER BY season_id, points DESC;

-- Statistics by season:
-- SELECT season_id, COUNT(*) as tournament_count FROM tournaments GROUP BY season_id ORDER BY season_id;
-- SELECT t.season_id, COUNT(m.id) as match_count 
-- FROM matches m JOIN tournaments t ON m.tournament_id = t.id 
-- GROUP BY t.season_id ORDER BY t.season_id;

-- ============================================================================
-- END OF SAMPLE DATA
-- ============================================================================
