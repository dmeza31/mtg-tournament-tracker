# Tournament Import Feature Guide

## Overview

The MTG Tournament Tracker now includes a complete tournament import system that allows tournament organizers to upload all tournament data (players, decks, matches, and games) in a single JSON file.

## Key Features

✅ **Single-File Import** - Upload one JSON file with all tournament data  
✅ **Auto-Creation** - Automatically creates missing players and deck archetypes  
✅ **Smart Matching** - Looks up existing players and decks by name  
✅ **Batch Processing** - Creates all entities in a single database transaction  
✅ **Full Validation** - Pydantic schema validation with detailed error messages  
✅ **Import Summary** - View counts of all created entities  

## How to Use

### Step 1: Prepare Your Tournament Data

Use the template file as a starting point:

**Location:** `imports/tournament_import_template.json`

Or refer to the complete example:

**Location:** `imports/tournament_import_example.json`

### Step 2: Fill in the Tournament Data

Your JSON file should include:

```json
{
  "season_id": 1,
  "tournament": {
    "name": "Friday Night Magic",
    "tournament_date": "2026-01-10",
    "location": "Local Game Store",
    "format": "Standard"
  },
  "players": [
    {"name": "Player Name", "email": "optional@email.com"}
  ],
  "decks": [
    {
      "name": "Deck Name",
      "color_identity": "WU",
      "archetype_type": "Control"
    }
  ],
  "matches": [
    {
      "round_number": 1,
      "player1_name": "Player Name",
      "player2_name": "Another Player",
      "player1_deck_name": "Deck Name",
      "player2_deck_name": "Another Deck",
      "games": [
        {
          "game_number": 1,
          "winner_name": "Player Name",
          "duration_minutes": 20
        }
      ]
    }
  ]
}
```

### Step 3: Upload via System Manager

1. Run the System Manager app (`streamlit run system-manager/app.py`, default http://localhost:8501)
2. Open the **"📤 Import"** tab
3. Click **"Browse files"** and select your JSON file
4. Review the preview and summary statistics
5. Click **"🚀 Import Tournament"** to process

### Step 4: View Results

After import, you'll see:
- ✅ Number of entities created (players, decks, matches, games)
- 📊 Success message with tournament details
- 🔄 Data automatically refreshed in other tabs

## JSON Format Details

### Required Fields

- **season_id** (integer): Must match an existing season in the database
- **tournament.name** (string): Tournament name
- **tournament.tournament_date** (string): Date in YYYY-MM-DD format
- **tournament.location** (string): Tournament location
- **tournament.format** (string): Magic format (Standard, Modern, etc.)

### Players Array

Each player object:
```json
{
  "name": "Player Name",
  "email": "optional@email.com"  // Optional
}
```

**Note:** If a player with the same name exists, the system will use the existing player instead of creating a duplicate.

### Decks Array

Each deck object:
```json
{
  "name": "Deck Archetype Name",
  "color_identity": "WU",        // W, U, B, R, G (any combination)
  "archetype_type": "Control"    // Aggro, Control, Combo, Midrange, Other
}
```

**Note:** If a deck with the same name exists, the system will use the existing deck.

### Matches Array

Each match object:
```json
{
  "round_number": 1,
  "player1_name": "Player 1",
  "player2_name": "Player 2",
  "player1_deck_name": "Deck 1",
  "player2_deck_name": "Deck 2",
  "games": [
    {
      "game_number": 1,
      "winner_name": "Player 1",
      "duration_minutes": 20
    }
  ]
}
```

**Important:** Player names and deck names must match exactly with the names in the players and decks arrays.

## Color Identity Reference

Use these abbreviations for deck colors:

- **W** - White
- **U** - Blue
- **B** - Black
- **R** - Red
- **G** - Green

Examples:
- `"WU"` - White-Blue (Azorius)
- `"BRG"` - Black-Red-Green (Jund)
- `"WUBRG"` - Five-color

## Archetype Types

Supported archetype types:
- `Aggro`
- `Control`
- `Combo`
- `Midrange`
- `Other`

## API Endpoint

The feature can also be accessed programmatically:

```bash
POST /api/v1/tournaments/import-complete
Content-Type: application/json

{
  "season_id": 1,
  "tournament": { ... },
  "players": [ ... ],
  "decks": [ ... ],
  "matches": [ ... ]
}
```

**Response:**
```json
{
  "success": true,
  "message": "Tournament imported successfully",
  "tournament_id": 5,
  "tournament_created": true,
  "players_created": 2,
  "decks_created": 2,
  "matches_created": 5,
  "games_created": 13
}
```

## Error Handling

The system validates:
- ✅ Season exists in database
- ✅ Valid date format
- ✅ Player names match in matches
- ✅ Deck names match in matches
- ✅ Unique game numbers per match
- ✅ Valid color identities
- ✅ Valid archetype types

If validation fails, you'll receive a detailed error message explaining what needs to be fixed.

## Example Workflow

### Tournament Organizer Scenario

1. **Before tournament:** Download `tournament_import_template.json`
2. **During tournament:** Record match results in the JSON file
3. **After tournament:** Upload the completed file via the System Manager import tab
4. **View results:** Check season standings and statistics

### Sample Tournament Data

The repository includes a complete example:

**File:** `imports/tournament_import_example.json`

**Contents:**
- 4 players (Sarah Connor, John Wick, Lara Croft, Nathan Drake)
- 4 different deck archetypes
- 5 matches across 3 rounds
- 13 total games with varying durations

You can use this as a reference when creating your own tournament files.

## Tips

💡 **Keep a Master File:** Save your tournament template with your regular players and decks pre-filled  
💡 **Validate JSON:** Use a JSON validator (like jsonlint.com) to check for syntax errors  
💡 **Test with Example:** Try importing the example file first to understand the workflow  
💡 **Backup Data:** Export your season data before importing large tournaments  
💡 **Round Robin Support:** For round-robin tournaments, simply add all matches to the matches array  

## Troubleshooting

### "Season not found"
- Verify the season_id exists in your database
- Check the season selector in the System Manager for valid IDs

### "Player name not found"
- Ensure player names in matches exactly match names in the players array
- Check for extra spaces or typos

### "Deck name not found"
- Ensure deck names in matches exactly match names in the decks array
- Names are case-sensitive

### "Invalid JSON"
- Check for missing commas between objects
- Verify all quotes are properly closed
- Ensure no trailing commas in arrays

### "Database error"
- Verify the API is running and connected to the database
- Check database connection in the services .env file

## Implementation Details

### Backend Components

**Files Modified:**
- `services/app/schemas.py` - Added 7 new Pydantic schemas
- `services/app/routers/tournaments.py` - Added import endpoint
- `services/app/crud/players.py` - Added `get_player_by_name()`
- `services/app/crud/decks.py` - Added `get_deck_by_name()`

### Frontend Components

**Files Modified:**
- `system-manager/app.py` - Added "Import" tab with file uploader

**Files Added:**
- `imports/tournament_import_template.json` - Blank template
- `imports/tournament_import_example.json` - Complete example

### Database Operations

The import process:
1. Validates season exists
2. Creates tournament record
3. Processes players (create new or lookup existing by name)
4. Processes decks (create new or lookup existing by name)
5. Creates matches with resolved player and deck IDs
6. Creates all games for each match
7. Returns summary with entity counts

All operations occur in a single database transaction - if any step fails, all changes are rolled back.

## Future Enhancements

Possible future additions:
- CSV format support
- Excel spreadsheet import
- Tournament bracket visualization
- Swiss pairing integration
- Multiple tournament import (batch seasons)
- Export tournament data to JSON

## Support

For issues or questions:
1. Check the example file for proper format
2. Validate your JSON syntax
3. Review error messages for specific issues
4. Check the API documentation at http://localhost:8000/docs

---

**Last Updated:** January 2026  
**Feature Version:** 1.0  
**Compatible with:** MTG Tournament Tracker v1.0+
