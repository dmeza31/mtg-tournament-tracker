# Season Standings Calculation

This document explains how player standings are calculated in the MTG Tournament Tracker.

## Overview

Season standings are calculated based on match performance across all tournaments in a season. Points are awarded based on the **tournament type**, with different events offering different point values for wins and draws.

## Tournament Types and Point Values

The system supports four tournament types with varying point structures:

| Tournament Type | Points per Win | Points per Draw | Description |
|----------------|----------------|-----------------|-------------|
| **Nationals** | 12 | 4 | Premier championship events |
| **Special Event** | 7 | 3 | Regional qualifiers, major competitions |
| **LGS Tournament** | 5 | 2 | Weekly/monthly local game store events (default) |
| **Online Tournament** | 3 | 0 | Online competitions |

## How Points Are Calculated

### Match Results

In Magic: The Gathering, matches are played as best-of-3 games:
- A player **wins** a match by winning 2 or more games
- A match is a **draw** if time expires or both players agree (typically 1-1-1 after 3 games)
- A player **loses** a match by winning fewer games than their opponent

### Points Assignment

For each match in a tournament:

1. **Match Win**: Player receives points based on the tournament type's `points_win` value
2. **Match Draw**: Both players receive points based on the tournament type's `points_draw` value
3. **Match Loss**: Player receives 0 points

### Season Total

A player's season standing is the **sum of all points** earned across all tournaments in that season.

## Examples

### Example 1: Player at Weekly LGS Tournament

**Tournament Type:** LGS Tournament (5 points/win, 2 points/draw)

**Results:**
- Round 1: Win vs Alice → **5 points**
- Round 2: Loss vs Bob → **0 points**
- Round 3: Draw vs Charlie → **2 points**

**Tournament Total:** 7 points

---

### Example 2: Player at Special Event

**Tournament Type:** Special Event (7 points/win, 3 points/draw)

**Results:**
- Round 1: Win vs Diana → **7 points**
- Round 2: Win vs Ethan → **7 points**
- Round 3: Draw vs Fiona → **3 points**

**Tournament Total:** 17 points

---

### Example 3: Season Standings Calculation

**Player: Alice Johnson**  
**Season: 2026 Q1 Standard Season**

| Tournament | Type | Matches | Points |
|-----------|------|---------|--------|
| January Standard Showdown | LGS Tournament | 2 wins, 1 loss | 10 points |
| February Championship Qualifier | Special Event | 1 win, 2 losses | 7 points |
| March Season Finale | Special Event | 3 wins, 1 draw | 24 points |

**Season Total:** 41 points

---

## Technical Implementation

### Database View

The standings are calculated using a PostgreSQL view called `season_standings`:

```sql
CREATE OR REPLACE VIEW season_standings AS
SELECT
    s.id AS season_id,
    s.name AS season_name,
    p.id AS player_id,
    p.name AS player_name,
    COUNT(DISTINCT t.id) AS tournaments_played,
    COUNT(DISTINCT m.id) AS matches_played,
    SUM(CASE WHEN mr.winner_id = p.id THEN COALESCE(tt.points_win, 3) ELSE 0 END) AS win_points,
    SUM(CASE WHEN mr.result_type = 'DRAW' THEN COALESCE(tt.points_draw, 1) ELSE 0 END) AS draw_points,
    SUM(
        CASE WHEN mr.winner_id = p.id THEN COALESCE(tt.points_win, 3)
             WHEN mr.result_type = 'DRAW' THEN COALESCE(tt.points_draw, 1)
             ELSE 0
        END
    ) AS points
FROM seasons s
CROSS JOIN players p
LEFT JOIN tournaments t ON t.season_id = s.id
LEFT JOIN tournament_types tt ON t.tournament_type_id = tt.id
LEFT JOIN matches m ON m.tournament_id = t.id AND (m.player1_id = p.id OR m.player2_id = p.id)
LEFT JOIN match_results mr ON mr.match_id = m.id
GROUP BY s.id, s.name, p.id, p.name
HAVING COUNT(DISTINCT m.id) > 0
ORDER BY s.id, points DESC, player_name;
```

### Fallback Values

If a tournament is missing a tournament type (should not happen with proper constraints), the system uses default fallback values:
- **3 points** for a win
- **1 point** for a draw

This ensures backward compatibility and prevents calculation errors.

---

## Match Results View

The `match_results` view determines the winner of each match based on game outcomes:

```sql
CREATE OR REPLACE VIEW match_results AS
SELECT
    m.id AS match_id,
    m.tournament_id,
    m.player1_id,
    m.player2_id,
    COUNT(CASE WHEN g.winner_id = m.player1_id AND g.game_result = 'WIN' THEN 1 END) AS player1_wins,
    COUNT(CASE WHEN g.winner_id = m.player2_id AND g.game_result = 'WIN' THEN 1 END) AS player2_wins,
    COUNT(CASE WHEN g.game_result = 'DRAW' THEN 1 END) AS draws,
    CASE
        WHEN COUNT(CASE WHEN g.winner_id = m.player1_id AND g.game_result = 'WIN' THEN 1 END) >
             COUNT(CASE WHEN g.winner_id = m.player2_id AND g.game_result = 'WIN' THEN 1 END)
        THEN m.player1_id
        WHEN COUNT(CASE WHEN g.winner_id = m.player2_id AND g.game_result = 'WIN' THEN 1 END) >
             COUNT(CASE WHEN g.winner_id = m.player1_id AND g.game_result = 'WIN' THEN 1 END)
        THEN m.player2_id
        ELSE NULL
    END AS winner_id,
    CASE
        WHEN COUNT(CASE WHEN g.winner_id = m.player1_id AND g.game_result = 'WIN' THEN 1 END) =
             COUNT(CASE WHEN g.winner_id = m.player2_id AND g.game_result = 'WIN' THEN 1 END)
        THEN 'DRAW'
        ELSE 'WIN'
    END AS result_type
FROM matches m
LEFT JOIN games g ON g.match_id = m.id
GROUP BY m.id, m.tournament_id, m.player1_id, m.player2_id;
```

---

## API Endpoints

### Get Season Standings

**Get all season standings:**
```bash
GET /api/v1/stats/season-standings
```

**Get standings for a specific season:**
```bash
GET /api/v1/stats/season-standings?season_id=1
# or
GET /api/v1/stats/season-standings/1
```

**Response Example:**
```json
[
  {
    "season_id": 1,
    "season_name": "2026 Q1 Standard Season",
    "player_id": 3,
    "player_name": "Charlie Davis",
    "tournaments_played": 3,
    "matches_played": 6,
    "win_points": 24,
    "draw_points": 2,
    "points": 26
  }
]
```

---

## UI Display

The Streamlit UI displays season standings with:

1. **Season selector** - Choose which season to view
2. **Standings table** - Shows players ranked by total points
3. **Key metrics:**
   - Player name
   - Total points (win_points + draw_points)
   - Tournaments played
   - Matches played
   - Win points breakdown
   - Draw points breakdown

Players are automatically ranked by points in descending order.

---

## Important Notes

### Default Tournament Type

When creating a tournament without specifying a type, the system defaults to **"LGS Tournament"** (5 points/win, 2 points/draw).

### Tournament Type Assignment

Tournament types can be specified when creating tournaments using:
- `tournament_type_id` - Direct reference by ID
- `tournament_type_name` - Case-insensitive name lookup (e.g., "LGS Tournament", "Nationals")

### Point Calculation Timing

- Points are calculated **dynamically** from the database view
- Standings update **immediately** when match results are recorded
- No manual recalculation is needed

### Draws in Online Tournaments

Note that **Online Tournament** type awards **0 points for draws**, reflecting the rarity of draws in online Magic platforms where time limits are strictly enforced.

---

## Related Documentation

- **Database Schema:** `database/01_schema.sql` - Tournament types table definition
- **Views:** `database/03_views.sql` - Season standings view implementation
- **Sample Data:** `database/05_sample_data.sql` - Tournament type seed data
- **API Documentation:** `services/README.md` - API endpoints for standings

For questions about standings calculation, refer to this document or check the database views in the `database/` folder.
