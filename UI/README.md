# MTG Tournament Tracker - Streamlit UI

Interactive dashboard for viewing tournament data, season standings, and deck statistics.

## Prerequisites

- Python 3.9+
- FastAPI backend running on http://localhost:8000

## Installation

```bash
# From UI directory
pip install -r requirements.txt
```

## Running the UI

```bash
# Make sure the API is running first (from services directory)
cd ../services
python -m uvicorn app.main:app --reload

# In another terminal, from UI directory
cd UI
streamlit run streamlit_app.py
```

## Features

### 📊 Season Standings
- View player rankings with points (3 per win, 1 per draw)
- Champion highlighting (Gold/Silver/Bronze for top 3)
- Switch between seasons using dropdown
- Display season information and dates

### 🎴 Deck Statistics
- Bar chart showing deck win rates by archetype
- **Deck filter** - Select a deck to see matchup analysis
- **Matchup win rates** - Color-coded table showing performance vs other decks
- **Visual matchup analysis** - Bar chart with win rate comparison
- Meta analysis with top 5 decks
- Pie chart for archetype distribution
- Detailed statistics table with all deck metrics

### 🏆 Tournament Results
- Browse tournaments by season
- View match results organized by rounds
- See individual game results within matches
- Tournament summary statistics

### 📤 Import Tournament
- **Complete tournament data import** - Upload a JSON file containing full tournament information
- **Auto-create entities** - Automatically creates missing players and deck archetypes
- **Smart matching** - Looks up existing players and decks by name
- **Batch import** - Import tournament, players, decks, matches, and games in one operation
- **Template files** - Use `tournament_import_template.json` as a starting point
- **Example file** - See `tournament_import_example.json` for a complete reference
- **Validation** - Built-in JSON schema validation and error reporting
- **Import summary** - View counts of created entities after import

## Tournament Import Format

The tournament import feature accepts JSON files with the following structure:

```json
{
  "season_id": 1,
  "tournament": {
    "name": "Friday Night Magic",
    "date": "2026-01-10",
    "location": "Local Game Store",
    "format": "Standard"
  },
  "players": [
    {"name": "Player 1", "email": "player1@email.com"}
  ],
  "decks": [
    {
      "name": "Temur Energy",
      "color_identity": "URG",
      "archetype_type": "Midrange"
    }
  ],
  "matches": [
    {
      "round_number": 1,
      "player1_name": "Player 1",
      "player2_name": "Player 2",
      "player1_deck_name": "Temur Energy",
      "player2_deck_name": "Esper Control",
      "games": [
        {
          "game_number": 1,
          "winner_name": "Player 1",
          "duration_minutes": 25
        }
      ]
    }
  ]
}
```

**Files available:**
- `tournament_import_template.json` - Blank template
- `tournament_import_example.json` - Complete example with sample data

## Configuration

### Local Development

The app automatically uses `http://localhost:8000/api/v1` for local development.

### Production/Railway Deployment

Set the `API_BASE_URL` environment variable:

```bash
export API_BASE_URL="https://your-api.railway.app/api/v1"
```

For Railway deployment instructions, see [RAILWAY_DEPLOYMENT.md](../RAILWAY_DEPLOYMENT.md) in the root directory.

**Railway Setup:**
- Service uses `Procfile` for automatic deployment
- Set `API_BASE_URL` environment variable to your FastAPI backend URL
- Railway automatically provides `$PORT` variable

## URL

The app will be available at: **http://localhost:8501**

## Troubleshooting

### Cannot connect to API
- Ensure the FastAPI backend is running
- Check that the API URL is correct
- Verify no firewall is blocking localhost connections

### Data not loading
- Click the "🔄 Refresh Data" button in the sidebar
- Check that you have data in your database
- Verify the database views are created (run `database/03_views.sql`)

## Project Structure

```
UI/
├── streamlit_app.py    # Main Streamlit application
├── requirements.txt    # Python dependencies
└── README.md          # This file
```
