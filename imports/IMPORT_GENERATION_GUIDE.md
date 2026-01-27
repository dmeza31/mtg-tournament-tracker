# Tournament Import Generation Guide

This guide explains how to use `generate_burro_imports.py` to convert MTG Melee tournament exports into the import format required by the MTG Tournament Tracker application.

## Overview

The `generate_burro_imports.py` script transforms raw tournament data exported from MTG Melee into a standardized JSON format that can be imported into the tournament tracking system. It handles:

- Player extraction and email generation
- Deck parsing and organization
- Match result processing with game-by-game winners
- Automatic filtering of byes and incomplete matches
- Draw handling (includes 1-1-0 draws with 2 games)

## Prerequisites

- Python 3.7+ with virtual environment activated
- MTG Melee tournament export file (JSON format)
- Season ID from your tournament tracking system
- Tournament name and location information

## Command-Line Usage

### Basic Syntax

```bash
python generate_burro_imports.py <input_file> <season_id> "Tournament Name" "Location"
```

### Required Parameters

| Parameter | Type | Description | Example |
|-----------|------|-------------|---------|
| `input_file` | Path | Path to MTG Melee JSON export | `imports/DataImport/OG_Monthly_Enero_2026.json` |
| `season_id` | Integer | Season ID number | `2` |
| `tournament_name` | String | Full tournament name (use quotes) | `"OG Monthly Enero 2026"` |
| `location` | String | Tournament location (use quotes) | `"Only Games"` |

### Optional Parameters

| Parameter | Type | Default | Description |
|-----------|------|---------|-------------|
| `-o, --output` | Path | Auto-generated | Output file path |
| `-f, --format` | String | `Premodern` | Tournament format |
| `-t, --tournament-type` | String | `LGS Tournament` | Tournament type |

## Examples

### Basic Usage (Auto-Generated Output)

Generate an import file with default settings. Output will be named `{input}_import.json`:

```bash
python generate_burro_imports.py imports/DataImport/OG_Monthly_Enero_2026.json 2 "OG Monthly Enero 2026" "Only Games"
```

**Output:** `imports/DataImport/OG_Monthly_Enero_2026_import.json`

### Custom Output Path

Specify a custom output location:

```bash
python generate_burro_imports.py imports/DataImport/tournament.json 2 "BurroSingles Monthly Enero 2026" "Burro Singles" -o imports/DataImport/custom_import.json
```

### Different Format

Generate an import for a Modern tournament:

```bash
python generate_burro_imports.py tournament.json 1 "Modern Weekly" "Only Games" -f Modern
```

### Custom Tournament Type

Generate an import for a competitive event:

```bash
python generate_burro_imports.py tournament.json 3 "Regional Championship" "Convention Center" -t "Competitive"
```

### Full Custom Options

Override all optional parameters:

```bash
python generate_burro_imports.py tournament.json 2 "Legacy Challenge" "Store Name" -o output/legacy_import.json -f Legacy -t "Competitive"
```

## Virtual Environment Activation

If using the project's virtual environment:

```bash
# Activate virtual environment
.venv\Scripts\activate

# Run script
python generate_burro_imports.py tournament.json 2 "Tournament Name" "Location"

# Deactivate when done
deactivate
```

## Output Format

The script generates a JSON file with the following structure:

```json
{
  "season_id": 2,
  "tournament": {
    "name": "OG Monthly Enero 2026",
    "tournament_date": "2026-01-24",
    "location": "Only Games",
    "format": "Premodern",
    "tournament_type_name": "LGS Tournament",
    "description": "OG Monthly Enero 2026 - Premodern Tournament"
  },
  "players": [...],
  "decks": [...],
  "matches": [...]
}
```

## Match Processing Rules

### Included Matches
- ✅ Regular matches with 2 competitors
- ✅ Matches with 2+ games played
- ✅ Draws (1-1-0 with 2 games)
- ✅ 2-0 sweeps
- ✅ 2-1 victories

### Excluded Matches
- ❌ Byes (single competitor)
- ❌ Matches with fewer than 2 games (concessions, early dropouts)
- ❌ Incomplete or corrupted match data

## Validation Output

When the script runs, it displays processing statistics:

```
Processing OG_Monthly_Enero_2026.json...
  Season ID: 2
  Tournament: OG Monthly Enero 2026
  Location: Only Games
  Format: Premodern
  Type: LGS Tournament
  Total records in source: 20
  Skipped (not 2 competitors): 4
  Skipped byes: 0
  Skipped incomplete matches (< 2 games): 2
  Valid matches: 14

✓ Created: imports/DataImport/OG_Monthly_Enero_2026_import.json
  - Players: 9
  - Decks: 9
  - Matches: 14
```

### Understanding the Counts

- **Total records**: All match records in source file
- **Skipped (not 2 competitors)**: Byes assigned by tournament software
- **Skipped byes**: Matches with "bye" in result string
- **Skipped incomplete**: Matches with fewer than 2 games (1-0, 0-0, etc.)
- **Valid matches**: Matches included in the output file

## Common Use Cases

### Scenario 1: New Monthly Tournament

You've just finished running a monthly tournament at your LGS and exported the data from MTG Melee.

```bash
python generate_burro_imports.py imports/DataImport/OG_Monthly_Febrero_2026.json 2 "OG Monthly Febrero 2026" "Only Games"
```

### Scenario 2: Regenerating Existing Import

You need to regenerate an import file with corrected information:

```bash
python generate_burro_imports.py imports/DataImport/BurroSingles_Monthly_Enero_2026.json 2 "BurroSingles Monthly Enero 2026" "Burro Singles" -o imports/DataImport/BurroSingles_Monthly_Enero_2026_import.json
```

### Scenario 3: Special Event

Processing a special competitive event with custom format:

```bash
python generate_burro_imports.py imports/DataImport/Championship_Q1_2026.json 2 "Q1 Championship 2026" "Only Games" -f Premodern -t "Competitive"
```

## Troubleshooting

### Error: Input file not found

**Solution:** Check the file path. Use absolute paths or ensure you're running the script from the correct directory.

```bash
# Use absolute path
python generate_burro_imports.py "C:\Users\...\tournament.json" 2 "Name" "Location"

# Or run from repository root
cd "C:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker"
python generate_burro_imports.py imports/DataImport/tournament.json 2 "Name" "Location"
```

### Error: Invalid JSON

**Solution:** Ensure the source file is a valid MTG Melee export. Open it in a text editor to verify it's properly formatted JSON.

### Fewer Matches Than Expected

**Solution:** Check the validation output. Matches may be excluded due to:
- Being byes (single competitor)
- Having fewer than 2 games played (concessions)
- Corrupted match data

Review the source file to verify match results.

### Email Generation

The script automatically generates placeholder emails from usernames:
- Username: `bard91r` → Email: `bard91r@email.com`

These are placeholders and can be updated manually in the import file or in the system after import.

## Next Steps

After generating the import file:

1. **Review the output** - Open the generated `_import.json` file to verify data
2. **Import via System Manager** - Use the `system-manager/app.py` application
3. **Navigate to Import tab** - Upload your generated JSON file
4. **Review preview** - Check player counts, matches, and tournament details
5. **Import** - Click the import button to add to your tournament tracker

See [imports/README.md](imports/README.md) for more details on the import process.

## Related Documentation

- [Tournament Import Format Reference](imports/IMPORT_FORMAT_REFERENCE.md) - Detailed field specifications
- [Tournament Import Guide](TOURNAMENT_IMPORT_GUIDE.md) - Manual import creation
- [Import Directory README](imports/README.md) - Import resources and examples

## Help Command

View all available options:

```bash
python generate_burro_imports.py --help
```

This displays:
- All required and optional parameters
- Parameter descriptions
- Usage examples
- Default values
