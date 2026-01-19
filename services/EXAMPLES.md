# API Usage Examples

Comprehensive examples for using the MTG Tournament Tracker API.

## Table of Contents

- [Setup](#setup)
- [Seasons](#seasons)
- [Tournament Types](#tournament-types)
- [Tournaments](#tournaments)
- [Players](#players)
- [Deck Archetypes](#deck-archetypes)
- [Matches & Games](#matches--games)
- [Batch Operations](#batch-operations)
- [Statistics](#statistics)
- [Python Examples](#python-examples)

## Setup

Base URL: `http://localhost:8000`

All examples use `curl` for command line and include Python `requests` alternatives.

---

## Seasons

### Create a Season

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/seasons" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "2026 Standard Season",
    "start_date": "2026-01-01",
    "end_date": "2026-03-31",
    "description": "Q1 2026 Standard tournament season"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/seasons",
    json={
        "name": "2026 Standard Season",
        "start_date": "2026-01-01",
        "end_date": "2026-03-31",
        "description": "Q1 2026 Standard tournament season"
    }
)
season = response.json()
print(f"Created season with ID: {season['id']}")
```

### Get All Seasons

**cURL:**
```bash
curl "http://localhost:8000/api/v1/seasons"
```

**Python:**
```python
response = requests.get("http://localhost:8000/api/v1/seasons")
seasons = response.json()
for season in seasons:
    print(f"{season['id']}: {season['name']}")
```

### Get Season by ID

**cURL:**
```bash
curl "http://localhost:8000/api/v1/seasons/1"
```

### Update Season

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/seasons/1" \
  -H "Content-Type: application/json" \
  -d '{
    "end_date": "2026-04-15",
    "description": "Extended season"
  }'
```

### Delete Season

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/seasons/1"
```

---

## Tournament Types

### Create a Tournament Type

Tournament types define point values for match wins and draws, allowing different competitive levels.

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/tournament-types" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Competitive",
    "points_win": 3,
    "points_draw": 1,
    "description": "Competitive level tournament with standard 3-1 points"
  }'
```

**Python:**
```python
import requests

response = requests.post(
    "http://localhost:8000/api/v1/tournament-types",
    json={
        "name": "Competitive",
        "points_win": 3,
        "points_draw": 1,
        "description": "Competitive level tournament with standard 3-1 points"
    }
)
tournament_type = response.json()
print(f"Created tournament type: {tournament_type['name']} (ID: {tournament_type['id']})")
```

### Get All Tournament Types

**cURL:**
```bash
curl "http://localhost:8000/api/v1/tournament-types"
```

**Python:**
```python
response = requests.get("http://localhost:8000/api/v1/tournament-types")
types = response.json()
for t in types:
    print(f"{t['id']}: {t['name']} - Win: {t['points_win']} pts, Draw: {t['points_draw']} pts")
```

### Get Tournament Type by ID

**cURL:**
```bash
curl "http://localhost:8000/api/v1/tournament-types/1"
```

### Update Tournament Type

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/tournament-types/1" \
  -H "Content-Type: application/json" \
  -d '{
    "points_win": 4,
    "points_draw": 2,
    "description": "Updated tournament type with increased points"
  }'
```

### Delete Tournament Type

**cURL:**
```bash
curl -X DELETE "http://localhost:8000/api/v1/tournament-types/1"
```

---

## Tournaments

### Create a Tournament

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/tournaments" \
  -H "Content-Type: application/json" \
  -d '{
    "season_id": 1,
    "tournament_type_id": 1,
    "name": "January Standard Showdown",
    "tournament_date": "2026-01-15",
    "location": "Local Game Store - Downtown",
    "format": "Standard",
    "description": "Weekly Standard tournament"
  }'
```

**Python:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/tournaments",
    json={
        "season_id": 1,
        "tournament_type_id": 1,
        "name": "January Standard Showdown",
        "tournament_date": "2026-01-15",
        "location": "Local Game Store - Downtown",
        "format": "Standard",
        "description": "Weekly Standard tournament"
    }
)
tournament = response.json()
print(f"Created tournament with ID: {tournament['id']}")
```

### Get All Tournaments

**cURL:**
```bash
# Get all tournaments
curl "http://localhost:8000/api/v1/tournaments"

# Filter by season
curl "http://localhost:8000/api/v1/tournaments?season_id=1"

# With pagination
curl "http://localhost:8000/api/v1/tournaments?skip=0&limit=10"
```

---

## Players

### Create a Tournament

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/tournaments" \
  -H "Content-Type: application/json" \
  -d '{
    "season_id": 1,
    "name": "January Standard Showdown",
    "tournament_date": "2026-01-15",
    "location": "Local Game Store - Downtown",
    "format": "Standard",
    "description": "Weekly Standard tournament"
  }'
```

**Python:**
```python
response = requests.post(
    "http://localhost:8000/api/v1/tournaments",
    json={
        "season_id": 1,
        "name": "January Standard Showdown",
        "tournament_date": "2026-01-15",
        "location": "Local Game Store - Downtown",
        "format": "Standard",
        "description": "Weekly Standard tournament"
    }
)
tournament = response.json()
print(f"Created tournament with ID: {tournament['id']}")
```

### Get All Tournaments

**cURL:**
```bash
# Get all tournaments
curl "http://localhost:8000/api/v1/tournaments"

# Filter by season
curl "http://localhost:8000/api/v1/tournaments?season_id=1"

# With pagination
curl "http://localhost:8000/api/v1/tournaments?skip=0&limit=10"
```

---

## Players

### Create a Player

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/players" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice.johnson@email.com",
    "active": true,
    "notes": "Experienced player"
  }'
```

**Python:**
```python
players_data = [
    {"name": "Alice Johnson", "email": "alice@email.com", "active": True},
    {"name": "Bob Smith", "email": "bob@email.com", "active": True},
    {"name": "Charlie Davis", "email": "charlie@email.com", "active": True}
]

player_ids = []
for player_data in players_data:
    response = requests.post(
        "http://localhost:8000/api/v1/players",
        json=player_data
    )
    player = response.json()
    player_ids.append(player['id'])
    print(f"Created player: {player['name']} (ID: {player['id']})")
```

### Get All Players

**cURL:**
```bash
# Get all players
curl "http://localhost:8000/api/v1/players"

# Get only active players
curl "http://localhost:8000/api/v1/players?active_only=true"
```

### Update Player

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/players/1" \
  -H "Content-Type: application/json" \
  -d '{
    "active": false,
    "notes": "Retired from tournaments"
  }'
```

---

## Deck Archetypes

### Create Deck Archetypes

**cURL:**
```bash
# Mono Red Aggro
curl -X POST "http://localhost:8000/api/v1/decks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mono Red Aggro",
    "color_identity": "R",
    "archetype_type": "Aggro",
    "description": "Fast aggressive red deck with burn spells"
  }'

# Azorius Control
curl -X POST "http://localhost:8000/api/v1/decks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Azorius Control",
    "color_identity": "WU",
    "archetype_type": "Control",
    "description": "Blue-white control with counterspells"
  }'
```

**Python:**
```python
decks_data = [
    {
        "name": "Mono Red Aggro",
        "color_identity": "R",
        "archetype_type": "Aggro",
        "description": "Fast aggressive red deck"
    },
    {
        "name": "Azorius Control",
        "color_identity": "WU",
        "archetype_type": "Control",
        "description": "Blue-white control deck"
    },
    {
        "name": "Golgari Midrange",
        "color_identity": "BG",
        "archetype_type": "Midrange",
        "description": "Black-green midrange"
    }
]

deck_ids = []
for deck_data in decks_data:
    response = requests.post(
        "http://localhost:8000/api/v1/decks",
        json=deck_data
    )
    deck = response.json()
    deck_ids.append(deck['id'])
    print(f"Created deck: {deck['name']} (ID: {deck['id']})")
```

### Get All Decks

**cURL:**
```bash
# Get all decks
curl "http://localhost:8000/api/v1/decks"

# Filter by archetype type
curl "http://localhost:8000/api/v1/decks?archetype_type=Aggro"
```

---

## Matches & Games

### Create a Match (Without Games)

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/matches" \
  -H "Content-Type: application/json" \
  -d '{
    "tournament_id": 1,
    "player1_id": 1,
    "player2_id": 2,
    "player1_deck_id": 1,
    "player2_deck_id": 2,
    "round_number": 1,
    "match_status": "COMPLETED"
  }'
```

### Add Games to a Match

**cURL:**
```bash
# Game 1 - Player 1 wins
curl -X POST "http://localhost:8000/api/v1/matches/1/games" \
  -H "Content-Type: application/json" \
  -d '{
    "game_number": 1,
    "winner_id": 1,
    "game_result": "WIN",
    "duration_minutes": 12
  }'

# Game 2 - Player 2 wins
curl -X POST "http://localhost:8000/api/v1/matches/1/games" \
  -H "Content-Type: application/json" \
  -d '{
    "game_number": 2,
    "winner_id": 2,
    "game_result": "WIN",
    "duration_minutes": 18
  }'

# Game 3 - Player 1 wins (match winner)
curl -X POST "http://localhost:8000/api/v1/matches/1/games" \
  -H "Content-Type: application/json" \
  -d '{
    "game_number": 3,
    "winner_id": 1,
    "game_result": "WIN",
    "duration_minutes": 15
  }'
```

### Get Match with Games

**cURL:**
```bash
curl "http://localhost:8000/api/v1/matches/1"
```

**Response:**
```json
{
  "id": 1,
  "tournament_id": 1,
  "player1_id": 1,
  "player2_id": 2,
  "player1_deck_id": 1,
  "player2_deck_id": 2,
  "round_number": 1,
  "match_status": "COMPLETED",
  "match_date": "2026-01-15T10:00:00Z",
  "games": [
    {
      "id": 1,
      "match_id": 1,
      "game_number": 1,
      "winner_id": 1,
      "game_result": "WIN",
      "duration_minutes": 12
    },
    {
      "id": 2,
      "match_id": 1,
      "game_number": 2,
      "winner_id": 2,
      "game_result": "WIN",
      "duration_minutes": 18
    },
    {
      "id": 3,
      "match_id": 1,
      "game_number": 3,
      "winner_id": 1,
      "game_result": "WIN",
      "duration_minutes": 15
    }
  ]
}
```

### Update a Match (players / round)

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/matches/1" \
  -H "Content-Type: application/json" \
  -d '{
    "player1_id": 3,
    "player2_id": 4,
    "round_number": 2
  }'
```

### Update a Game (winner / result)

**cURL:**
```bash
curl -X PUT "http://localhost:8000/api/v1/matches/1/games/2" \
  -H "Content-Type: application/json" \
  -d '{
    "winner_id": 3,
    "game_result": "WIN"
  }'
```

### Add a Game (if less than 3 exist)

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/matches/1/games" \
  -H "Content-Type: application/json" \
  -d '{
    "game_number": 3,
    "winner_id": 3,
    "game_result": "DRAW",
    "duration_minutes": 20,
    "notes": "Time expired"
  }'
```

### Get Matches with Filters

**cURL:**
```bash
# Get matches for a tournament
curl "http://localhost:8000/api/v1/matches?tournament_id=1"

# Get matches for a player
curl "http://localhost:8000/api/v1/matches?player_id=1"

# With pagination
curl "http://localhost:8000/api/v1/matches?skip=0&limit=10"
```

---

## Batch Operations

### Batch Create Matches (Recommended)

This is the **most efficient way** to insert multiple matches with games.

**cURL:**
```bash
curl -X POST "http://localhost:8000/api/v1/matches/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "matches": [
      {
        "tournament_id": 1,
        "player1_id": 1,
        "player2_id": 2,
        "player1_deck_id": 1,
        "player2_deck_id": 2,
        "round_number": 1,
        "match_status": "COMPLETED",
        "games": [
          {"game_number": 1, "winner_id": 1, "game_result": "WIN", "duration_minutes": 12},
          {"game_number": 2, "winner_id": 2, "game_result": "WIN", "duration_minutes": 18},
          {"game_number": 3, "winner_id": 1, "game_result": "WIN", "duration_minutes": 15}
        ]
      },
      {
        "tournament_id": 1,
        "player1_id": 3,
        "player2_id": 4,
        "player1_deck_id": 3,
        "player2_deck_id": 4,
        "round_number": 1,
        "match_status": "COMPLETED",
        "games": [
          {"game_number": 1, "winner_id": 3, "game_result": "WIN", "duration_minutes": 20},
          {"game_number": 2, "winner_id": 3, "game_result": "WIN", "duration_minutes": 22}
        ]
      }
    ]
  }'
```

**Python:**
```python
batch_data = {
    "matches": [
        {
            "tournament_id": 1,
            "player1_id": 1,
            "player2_id": 2,
            "player1_deck_id": 1,
            "player2_deck_id": 2,
            "round_number": 1,
            "match_status": "COMPLETED",
            "games": [
                {"game_number": 1, "winner_id": 1, "game_result": "WIN", "duration_minutes": 12},
                {"game_number": 2, "winner_id": 2, "game_result": "WIN", "duration_minutes": 18},
                {"game_number": 3, "winner_id": 1, "game_result": "WIN", "duration_minutes": 15}
            ]
        },
        {
            "tournament_id": 1,
            "player1_id": 3,
            "player2_id": 4,
            "player1_deck_id": 3,
            "player2_deck_id": 4,
            "round_number": 1,
            "match_status": "COMPLETED",
            "games": [
                {"game_number": 1, "winner_id": 3, "game_result": "WIN", "duration_minutes": 20},
                {"game_number": 2, "winner_id": 3, "game_result": "WIN", "duration_minutes": 22}
            ]
        }
    ]
}

response = requests.post(
    "http://localhost:8000/api/v1/matches/batch",
    json=batch_data
)
result = response.json()
print(f"Success: {result['success_count']}, Failed: {result['failed_count']}")
print(f"Created match IDs: {result['created_match_ids']}")
if result['errors']:
    print(f"Errors: {result['errors']}")
```

**Response:**
```json
{
  "success_count": 2,
  "failed_count": 0,
  "created_match_ids": [1, 2],
  "errors": []
}
```

### Loading Tournament Results from CSV

**Python Example:**
```python
import csv
import requests

def load_tournament_from_csv(csv_file, tournament_id):
    """Load match results from CSV file."""
    matches = []
    
    with open(csv_file, 'r') as f:
        reader = csv.DictReader(f)
        for row in reader:
            match = {
                "tournament_id": tournament_id,
                "player1_id": int(row['player1_id']),
                "player2_id": int(row['player2_id']),
                "player1_deck_id": int(row['player1_deck_id']),
                "player2_deck_id": int(row['player2_deck_id']),
                "round_number": int(row['round_number']),
                "match_status": "COMPLETED",
                "games": [
                    {
                        "game_number": 1,
                        "winner_id": int(row['game1_winner_id']),
                        "game_result": "WIN",
                        "duration_minutes": int(row['game1_duration'])
                    },
                    {
                        "game_number": 2,
                        "winner_id": int(row['game2_winner_id']),
                        "game_result": "WIN",
                        "duration_minutes": int(row['game2_duration'])
                    }
                ]
            }
            
            # Add game 3 if exists
            if row.get('game3_winner_id'):
                match['games'].append({
                    "game_number": 3,
                    "winner_id": int(row['game3_winner_id']),
                    "game_result": "WIN",
                    "duration_minutes": int(row['game3_duration'])
                })
            
            matches.append(match)
    
    # Batch insert
    response = requests.post(
        "http://localhost:8000/api/v1/matches/batch",
        json={"matches": matches}
    )
    return response.json()

# Usage
result = load_tournament_from_csv('tournament_results.csv', tournament_id=1)
print(f"Loaded {result['success_count']} matches")
```

---

## Statistics

### Get Player Statistics

**cURL:**
```bash
# Get all player stats
curl "http://localhost:8000/api/v1/stats/players"

# Get specific player stats
curl "http://localhost:8000/api/v1/stats/players/1"
```

**Response:**
```json
[
  {
    "player_id": 1,
    "player_name": "Alice Johnson",
    "total_matches": 10,
    "matches_won": 7,
    "matches_drawn": 0,
    "matches_lost": 3,
    "win_rate_percentage": 70.0,
    "decks_played": 2,
    "tournaments_played": 3
  }
]
```

**Python:**
```python
# Get top 5 players by win rate
response = requests.get("http://localhost:8000/api/v1/stats/players")
players = response.json()

# Sort by win rate
sorted_players = sorted(
    players, 
    key=lambda p: p['win_rate_percentage'] or 0, 
    reverse=True
)

print("Top 5 Players by Win Rate:")
for i, player in enumerate(sorted_players[:5], 1):
    print(f"{i}. {player['player_name']}: {player['win_rate_percentage']}% "
          f"({player['matches_won']}-{player['matches_lost']})")
```

### Get Deck Statistics

**cURL:**
```bash
# Get all deck stats
curl "http://localhost:8000/api/v1/stats/decks"

# Get specific deck stats
curl "http://localhost:8000/api/v1/stats/decks/1"
```

**Response:**
```json
[
  {
    "deck_id": 1,
    "deck_name": "Mono Red Aggro",
    "color_identity": "R",
    "archetype_type": "Aggro",
    "total_matches": 15,
    "matches_won": 9,
    "matches_drawn": 1,
    "matches_lost": 5,
    "win_rate_percentage": 60.0,
    "unique_players": 3,
    "tournaments_played": 4
  }
]
```

### Get Deck Matchup Statistics

**cURL:**
```bash
# Get all matchups
curl "http://localhost:8000/api/v1/stats/matchups"

# Get specific matchup (Mono Red Aggro vs Azorius Control)
curl "http://localhost:8000/api/v1/stats/matchups/1/2"
```

**Response:**
```json
{
  "deck_a_id": 1,
  "deck_a_name": "Mono Red Aggro",
  "deck_b_id": 2,
  "deck_b_name": "Azorius Control",
  "total_matches": 5,
  "deck_a_wins": 3,
  "draws": 0,
  "deck_a_losses": 2,
  "deck_a_win_rate_percentage": 60.0,
  "deck_b_win_rate_percentage": 40.0
}
```

**Python - Analyze Meta:**
```python
# Get all deck statistics
response = requests.get("http://localhost:8000/api/v1/stats/decks")
decks = response.json()

# Calculate meta share
total_matches = sum(d['total_matches'] for d in decks)
print("Current Meta Breakdown:\n")

for deck in sorted(decks, key=lambda d: d['total_matches'], reverse=True):
    meta_share = (deck['total_matches'] / total_matches * 100) if total_matches > 0 else 0
    print(f"{deck['deck_name']:25} - {meta_share:5.1f}% meta, "
          f"{deck['win_rate_percentage']:5.1f}% win rate, "
          f"{deck['total_matches']} matches")
```

### Get Season Standings

**cURL:**
```bash
# Get all season standings
curl "http://localhost:8000/api/v1/stats/season-standings"

# Get standings for specific season
curl "http://localhost:8000/api/v1/stats/season-standings?season_id=1"

# Alternative: Get specific season standings
curl "http://localhost:8000/api/v1/stats/season-standings/1"
```

**Response:**
```json
[
  {
    "season_id": 1,
    "season_name": "2026 Standard Season",
    "player_id": 1,
    "player_name": "Alice Johnson",
    "matches_played": 12,
    "wins": 9,
    "draws": 1,
    "losses": 2,
    "points": 28
  },
  {
    "season_id": 1,
    "season_name": "2026 Standard Season",
    "player_id": 3,
    "player_name": "Charlie Davis",
    "matches_played": 10,
    "wins": 7,
    "draws": 0,
    "losses": 3,
    "points": 21
  },
  {
    "season_id": 1,
    "season_name": "2026 Standard Season",
    "player_id": 2,
    "player_name": "Bob Smith",
    "matches_played": 11,
    "wins": 5,
    "draws": 3,
    "losses": 3,
    "points": 18
  }
]
```

**Python - Display Season Standings:**
```python
# Get standings for season 1
response = requests.get("http://localhost:8000/api/v1/stats/season-standings/1")
standings = response.json()

print("Season Standings")
print("=" * 70)
print(f"{'Pos':<5} {'Player':<20} {'MP':<5} {'W':<5} {'D':<5} {'L':<5} {'Points':<7}")
print("-" * 70)

for i, player in enumerate(standings, 1):
    print(f"{i:<5} {player['player_name']:<20} {player['matches_played']:<5} "
          f"{player['wins']:<5} {player['draws']:<5} {player['losses']:<5} "
          f"{player['points']:<7}")

# Calculate season champion
if standings:
    champion = standings[0]
    print(f"\nSeason Champion: {champion['player_name']} with {champion['points']} points!")
```

**Python - Compare All Seasons:**
```python
# Get all season standings
response = requests.get("http://localhost:8000/api/v1/stats/season-standings")
all_standings = response.json()

# Group by season
from itertools import groupby

standings_by_season = {}
for season_id, group in groupby(all_standings, key=lambda x: x['season_id']):
    standings_by_season[season_id] = list(group)

# Display each season's top 3
for season_id, standings in standings_by_season.items():
    season_name = standings[0]['season_name']
    print(f"\n{season_name} - Top 3:")
    for i, player in enumerate(standings[:3], 1):
        print(f"  {i}. {player['player_name']}: {player['points']} points "
              f"({player['wins']}-{player['draws']}-{player['losses']})")
```

---

## Python Examples

### Complete Tournament Entry Script

```python
import requests
from typing import List, Dict

BASE_URL = "http://localhost:8000/api/v1"

class MTGTournamentAPI:
    def __init__(self, base_url: str = BASE_URL):
        self.base_url = base_url
    
    def create_season(self, name: str, start_date: str, end_date: str = None):
        response = requests.post(
            f"{self.base_url}/seasons",
            json={"name": name, "start_date": start_date, "end_date": end_date}
        )
        return response.json()
    
    def create_tournament(self, season_id: int, name: str, date: str, location: str, format: str):
        response = requests.post(
            f"{self.base_url}/tournaments",
            json={
                "season_id": season_id,
                "name": name,
                "tournament_date": date,
                "location": location,
                "format": format
            }
        )
        return response.json()
    
    def create_player(self, name: str, email: str = None):
        response = requests.post(
            f"{self.base_url}/players",
            json={"name": name, "email": email, "active": True}
        )
        return response.json()
    
    def create_deck(self, name: str, color: str, archetype_type: str):
        response = requests.post(
            f"{self.base_url}/decks",
            json={
                "name": name,
                "color_identity": color,
                "archetype_type": archetype_type
            }
        )
        return response.json()
    
    def batch_create_matches(self, matches: List[Dict]):
        response = requests.post(
            f"{self.base_url}/matches/batch",
            json={"matches": matches}
        )
        return response.json()
    
    def get_player_stats(self):
        response = requests.get(f"{self.base_url}/stats/players")
        return response.json()
    
    def get_deck_matchup(self, deck_a_id: int, deck_b_id: int):
        response = requests.get(f"{self.base_url}/stats/matchups/{deck_a_id}/{deck_b_id}")
        return response.json()

# Usage example
api = MTGTournamentAPI()

# Create season
season = api.create_season("2026 Q1 Season", "2026-01-01", "2026-03-31")
print(f"Created season: {season['name']}")

# Create tournament
tournament = api.create_tournament(
    season_id=season['id'],
    name="Weekly Standard",
    date="2026-01-15",
    location="Local Game Store",
    format="Standard"
)
print(f"Created tournament: {tournament['name']}")

# Get statistics
stats = api.get_player_stats()
for player in stats:
    print(f"{player['player_name']}: {player['matches_won']}-{player['matches_lost']}")
```

### Generate Tournament Report

```python
import requests
from datetime import datetime

def generate_tournament_report(tournament_id: int):
    """Generate a comprehensive tournament report."""
    base_url = "http://localhost:8000/api/v1"
    
    # Get tournament details
    tournament = requests.get(f"{base_url}/tournaments/{tournament_id}").json()
    
    # Get all matches for tournament
    matches = requests.get(f"{base_url}/matches?tournament_id={tournament_id}").json()
    
    # Get player stats
    all_player_stats = requests.get(f"{base_url}/stats/players").json()
    
    print(f"\n{'='*60}")
    print(f"TOURNAMENT REPORT: {tournament['name']}")
    print(f"Date: {tournament['tournament_date']}")
    print(f"Location: {tournament['location']}")
    print(f"{'='*60}\n")
    
    print(f"Total Matches: {len(matches)}\n")
    
    # Calculate tournament-specific stats
    player_records = {}
    for match in matches:
        # This is simplified - you'd need to fetch games and determine winner
        pass
    
    print("\nPlayer Performance:")
    for stats in all_player_stats:
        print(f"{stats['player_name']:20} - "
              f"Win Rate: {stats['win_rate_percentage']:5.1f}% - "
              f"Record: {stats['matches_won']}-{stats['matches_drawn']}-{stats['matches_lost']}")

# Usage
generate_tournament_report(tournament_id=1)
```

---

## Error Handling Examples

### Handling Validation Errors

**Python:**
```python
try:
    response = requests.post(
        "http://localhost:8000/api/v1/players",
        json={"name": "", "email": "invalid"}  # Invalid data
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 422:
        errors = e.response.json()
        print("Validation errors:")
        for error in errors.get('errors', []):
            print(f"  - {error['field']}: {error['message']}")
```

### Handling Conflicts

**Python:**
```python
try:
    response = requests.post(
        "http://localhost:8000/api/v1/players",
        json={"name": "John Doe", "email": "existing@email.com"}
    )
    response.raise_for_status()
except requests.exceptions.HTTPError as e:
    if e.response.status_code == 409:
        print("Conflict: Email already exists")
        error_data = e.response.json()
        print(f"Detail: {error_data['detail']}")
```

---

## Testing the API

### Quick Smoke Test

**Bash Script:**
```bash
#!/bin/bash
BASE_URL="http://localhost:8000/api/v1"

echo "Testing MTG Tournament API..."

# Test health endpoint
echo "1. Health check..."
curl -s "$BASE_URL/../health" | jq

# Test creating a season
echo "2. Creating season..."
SEASON_ID=$(curl -s -X POST "$BASE_URL/seasons" \
  -H "Content-Type: application/json" \
  -d '{"name":"Test Season","start_date":"2026-01-01"}' \
  | jq -r '.id')
echo "Created season ID: $SEASON_ID"

# Test getting seasons
echo "3. Getting seasons..."
curl -s "$BASE_URL/seasons" | jq

echo "All tests completed!"
```

---

For more information, see the [README.md](README.md) and visit the interactive API documentation at http://localhost:8000/docs
