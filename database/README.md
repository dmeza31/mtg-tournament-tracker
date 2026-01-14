# MTG Tournament Tracking System - PostgreSQL Database

A comprehensive PostgreSQL database for tracking Magic the Gathering tournament matches, including best-of-3 game results, player performance, and deck archetype statistics across tournament seasons.

## Features

- **Best-of-3 Match Tracking**: Separate tables for matches and individual games
- **Deck Archetype Management**: Normalized deck archetypes with metadata
- **Player Statistics**: Track wins, draws, and losses by player
- **Deck Statistics**: Analyze performance of deck archetypes
- **Matchup Analysis**: Calculate win rates between specific deck pairings
- **Tournament Organization**: Season and tournament hierarchy
- **Optimized Queries**: Indexes designed for common query patterns

## Database Schema

### Core Tables

1. **seasons** - Tournament seasons (e.g., "2026 Standard Season")
2. **tournaments** - Individual tournaments within seasons
3. **players** - Player information and registration
4. **deck_archetypes** - Deck archetypes (e.g., "Mono Red Aggro", "Azorius Control")
5. **matches** - Match-level information (best-of-3)
6. **games** - Individual game results within matches

### Relationships

- Each tournament belongs to a season
- Each match belongs to a tournament and involves two players with two decks
- Each match contains 1-3 games (best-of-3 format)
- Match winners are determined by first player to win 2 games

## Setup Instructions

### Prerequisites

- PostgreSQL 12 or higher
- Database client (psql, pgAdmin, DBeaver, etc.)

### Installation

#### Method 1: Using psql Command Line (Linux/Mac/Windows with psql in PATH)

1. **Create Database**:
   ```bash
   createdb mtg_tournaments
   ```

2. **Run Schema Script**:
   ```bash
   psql -d mtg_tournaments -f 01_schema.sql
   ```

3. **Create Indexes**:
   ```bash
   psql -d mtg_tournaments -f 02_indexes.sql
   ```

4. **Create Views**:
   ```bash
   psql -d mtg_tournaments -f 03_views.sql
   ```

5. **Load Sample Data** (optional):
   ```bash
   psql -d mtg_tournaments -f 05_sample_data.sql
   ```

#### Method 2: Using PowerShell on Windows

If `psql` is not in your PATH, use the full path to PostgreSQL bin directory:

```powershell
# Set PostgreSQL password (replace 'postgres' with your password)
$env:PGPASSWORD='postgres'

# Navigate to database directory
cd "path\to\database"

# Run each script in order
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d mtg_tournaments -f "01_schema.sql"
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d mtg_tournaments -f "02_indexes.sql"
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d mtg_tournaments -f "03_views.sql"
& "C:\Program Files\PostgreSQL\16\bin\psql.exe" -U postgres -d mtg_tournaments -f "05_sample_data.sql"
```

**Note**: Adjust the PostgreSQL version number (16) in the path if you have a different version installed.

#### Method 3: Using Bash/Git Bash on Windows

If you have Git Bash or WSL installed on Windows:

```bash
# Set PostgreSQL password (replace 'postgres' with your password)
export PGPASSWORD='postgres'

# Navigate to database directory
cd /c/path/to/database

# Option A: If psql is in your PATH
psql -U postgres -d mtg_tournaments -f "01_schema.sql"
psql -U postgres -d mtg_tournaments -f "02_indexes.sql"
psql -U postgres -d mtg_tournaments -f "03_views.sql"
psql -U postgres -d mtg_tournaments -f "05_sample_data.sql"

# Option B: If psql is not in PATH, use full path (adjust version number)
"/c/Program Files/PostgreSQL/16/bin/psql.exe" -U postgres -d mtg_tournaments -f "01_schema.sql"
"/c/Program Files/PostgreSQL/16/bin/psql.exe" -U postgres -d mtg_tournaments -f "02_indexes.sql"
"/c/Program Files/PostgreSQL/16/bin/psql.exe" -U postgres -d mtg_tournaments -f "03_views.sql"
"/c/Program Files/PostgreSQL/16/bin/psql.exe" -U postgres -d mtg_tournaments -f "05_sample_data.sql"

# Or run all at once
for file in 01_schema.sql 02_indexes.sql 03_views.sql 05_sample_data.sql; do
  psql -U postgres -d mtg_tournaments -f "$file"
done
```

#### Method 4: Using pgAdmin (GUI)

1. Open pgAdmin and connect to your PostgreSQL server
2. Right-click on "Databases" → Create → Database
3. Name: `mtg_tournaments`
4. Right-click on the new database → Query Tool
5. Open each SQL file using the folder icon and execute:
   - `01_schema.sql`
   - `02_indexes.sql`
   - `03_views.sql`
   - `05_sample_data.sql` (optional)

#### Method 5: Using DBeaver or Other SQL Client

1. Create new connection to PostgreSQL
2. Create new database: `mtg_tournaments`
3. Open SQL Script and execute files in order:
   - `01_schema.sql`
   - `02_indexes.sql`
   - `03_views.sql`
   - `05_sample_data.sql` (optional)

### Verification

After installation, verify the setup:

```sql
-- Check tables
SELECT table_name FROM information_schema.tables 
WHERE table_schema = 'public';

-- Check views
SELECT table_name FROM information_schema.views 
WHERE table_schema = 'public';

-- Test with sample query
SELECT * FROM player_statistics;
```

## Usage

### Available Views

The database includes several pre-built views for common analytics:

- **match_results** - Aggregates games to determine match winners
- **player_statistics** - Win/draw/loss stats for each player
- **deck_statistics** - Win/draw/loss stats for each deck archetype
- **deck_matchups** - Head-to-head performance between deck pairs
- **player_deck_performance** - Performance of each player with specific decks
- **tournament_summary** - Overview statistics for each tournament
- **season_standings** - Player rankings by season with points (3 per win, 1 per draw)

### Common Queries

See [04_sample_queries.sql](04_sample_queries.sql) for examples of:

#### Player Statistics
- Number of matches won grouped by player
- Number of matches drawn grouped by player
- Number of matches lost grouped by player
- Complete player records with win rates

#### Deck Statistics
- Number of matches won grouped by deck
- Number of matches drawn grouped by deck
- Number of matches lost grouped by deck
- Meta analysis (deck popularity and performance)

#### Matchup Analysis
- Win rate of deck X vs deck Y
- All matchups for a specific deck
- Most favorable matchups
- Most played matchups

### Example Queries

**Get player statistics:**
```sql
SELECT player_name, matches_won, matches_drawn, matches_lost, win_rate_percentage
FROM player_statistics
ORDER BY win_rate_percentage DESC;
```

**Get deck statistics:**
```sql
SELECT deck_name, matches_won, matches_drawn, matches_lost, win_rate_percentage
FROM deck_statistics
ORDER BY win_rate_percentage DESC;
```

**Get matchup win rate (Mono Red Aggro vs Azorius Control):**
```sql
SELECT deck_a_name, deck_b_name, total_matches, 
       deck_a_win_rate_percentage, deck_b_win_rate_percentage
FROM deck_matchups
WHERE deck_a_name = 'Mono Red Aggro' AND deck_b_name = 'Azorius Control';
```

**Get season standings:**
```sql
SELECT season_name, player_name, matches_played, wins, draws, losses, points
FROM season_standings
WHERE season_id = 1
ORDER BY points DESC, wins DESC;
```

## File Structure

```
database/
├── 01_schema.sql          # Database schema with all tables and constraints
├── 02_indexes.sql         # Performance indexes for common queries
├── 03_views.sql           # Pre-built views for analytics
├── 04_sample_queries.sql  # Example queries for all requested analytics
├── 05_sample_data.sql     # Sample tournament data for testing
└── README.md              # This file
```

## Data Model

### Match Flow
1. Create a match record linking tournament, two players, and their decks
2. Record individual game results (best-of-3)
3. Match winner is automatically determined from game results (first to 2 wins)
4. Statistics are calculated through views

### Recording a Match

```sql
-- 1. Insert match
INSERT INTO matches (tournament_id, player1_id, player2_id, player1_deck_id, player2_deck_id, round_number)
VALUES (1, 1, 2, 1, 2, 1);

-- 2. Record games (assuming match_id = 1)
INSERT INTO games (match_id, game_number, winner_id, game_result) VALUES
(1, 1, 1, 'WIN'),  -- Player 1 wins game 1
(1, 2, 2, 'WIN'),  -- Player 2 wins game 2
(1, 3, 1, 'WIN');  -- Player 1 wins game 3 (match winner)
```

## Performance Considerations

### Indexes
The database includes optimized indexes for:
- Player-based aggregations
- Deck-based aggregations
- Deck matchup queries
- Tournament lookups
- Date range queries

### Materialized Views (Optional)
For very large datasets, consider creating materialized views:
```sql
CREATE MATERIALIZED VIEW mv_deck_statistics AS
SELECT * FROM deck_statistics;

-- Refresh periodically
REFRESH MATERIALIZED VIEW mv_deck_statistics;
```

## Extending the Schema

### Adding New Fields

**Track sideboard games:**
```sql
ALTER TABLE games ADD COLUMN is_sideboard_game BOOLEAN DEFAULT FALSE;
```

**Track play/draw:**
```sql
ALTER TABLE games ADD COLUMN player_on_play INTEGER REFERENCES players(id);
```

**Track mulligan counts:**
```sql
ALTER TABLE games ADD COLUMN player1_mulligans INTEGER;
ALTER TABLE games ADD COLUMN player2_mulligans INTEGER;
```

## Maintenance

### Regular Tasks

1. **Analyze tables** after bulk inserts:
   ```sql
   ANALYZE matches;
   ANALYZE games;
   ```

2. **Monitor index usage**:
   ```sql
   SELECT * FROM pg_stat_user_indexes;
   ```

3. **Vacuum** for cleanup:
   ```sql
   VACUUM ANALYZE;
   ```

## License

This database schema is provided as-is for use in Magic the Gathering tournament tracking applications.

## Support

For issues or questions, please refer to the sample queries and documentation within each SQL file.
