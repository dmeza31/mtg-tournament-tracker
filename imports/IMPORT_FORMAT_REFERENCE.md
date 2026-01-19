# Quick Reference: Tournament Import JSON Format

## Minimal Valid Example

```json
{
  "season_id": 1,
  "tournament": {
    "name": "Weekly Tournament",
    "tournament_date": "2026-01-15",
    "location": "Game Store",
    "format": "Standard"
  },
  "players": [
    {"name": "Alice"},
    {"name": "Bob"}
  ],
  "decks": [
    {"name": "Aggro Deck", "color_identity": "R", "archetype_type": "Aggro"},
    {"name": "Control Deck", "color_identity": "UB", "archetype_type": "Control"}
  ],
  "matches": [
    {
      "round_number": 1,
      "player1_name": "Alice",
      "player2_name": "Bob",
      "player1_deck_name": "Aggro Deck",
      "player2_deck_name": "Control Deck",
      "games": [
        {"game_number": 1, "winner_name": "Alice", "duration_minutes": 15},
        {"game_number": 2, "winner_name": "Bob", "duration_minutes": 20},
        {"game_number": 3, "winner_name": "Alice", "duration_minutes": 12}
      ]
    }
  ]
}
```

## Field Reference

### Top Level
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| season_id | integer | Yes | ID of existing season |
| tournament | object | Yes | Tournament information |
| players | array | Yes | List of players |
| decks | array | Yes | List of deck archetypes |
| matches | array | Yes | List of matches |

### Tournament Object
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Tournament name |
| tournament_date | string | Yes | Date (YYYY-MM-DD) |
| location | string | Yes | Tournament location |
| format | string | Yes | Magic format |
| tournament_type_name | string | No | Defaults to "LGS Tournament" if omitted |

### Player Object
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Player name |
| email | string | No | Player email |

### Deck Object
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| name | string | Yes | Deck archetype name |
| color_identity | string | Yes | W, U, B, R, G combination |
| archetype_type | string | Yes | Aggro, Control, Combo, Midrange, Other |

### Match Object
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| round_number | integer | Yes | Round number |
| player1_name | string | Yes | First player (must match players array) |
| player2_name | string | Yes | Second player (must match players array) |
| player1_deck_name | string | Yes | Player 1's deck (must match decks array) |
| player2_deck_name | string | Yes | Player 2's deck (must match decks array) |
| games | array | Yes | List of games (1-3 games) |

### Game Object
| Field | Type | Required | Description |
|-------|------|----------|-------------|
| game_number | integer | Yes | Game number (1, 2, or 3) |
| winner_name | string | Yes | Winner (must be player1 or player2) |
| duration_minutes | integer | No | Game duration in minutes |

## Color Identity Codes

| Code | Colors | Guild/Shard Name |
|------|--------|------------------|
| W | White | Mono-White |
| U | Blue | Mono-Blue |
| B | Black | Mono-Black |
| R | Red | Mono-Red |
| G | Green | Mono-Green |
| WU | White-Blue | Azorius |
| WB | White-Black | Orzhov |
| WR | White-Red | Boros |
| WG | White-Green | Selesnya |
| UB | Blue-Black | Dimir |
| UR | Blue-Red | Izzet |
| UG | Blue-Green | Simic |
| BR | Black-Red | Rakdos |
| BG | Black-Green | Golgari |
| RG | Red-Green | Gruul |
| WUB | Esper | Esper |
| WUR | Jeskai | Jeskai |
| WUG | Bant | Bant |
| WBR | Mardu | Mardu |
| WBG | Abzan | Abzan |
| WRG | Naya | Naya |
| UBR | Grixis | Grixis |
| UBG | Sultai | Sultai |
| URG | Temur | Temur |
| BRG | Jund | Jund |
| WUBR | Four-color | Four-color |
| WUBRG | Five-color | Five-color |

## Archetype Types

- `Aggro` - Fast, aggressive strategies
- `Control` - Reactive, late-game focused
- `Combo` - Win through card combinations
- `Midrange` - Balanced value strategies
- `Other` - Other strategies (Ramp, Tokens, etc.)

## Common Mistakes

❌ **Wrong:** Player names don't match
```json
"players": [{"name": "Alice Smith"}],
"matches": [{"player1_name": "Alice"}]  // Missing "Smith"
```

✅ **Correct:**
```json
"players": [{"name": "Alice Smith"}],
"matches": [{"player1_name": "Alice Smith"}]
```

---

❌ **Wrong:** Invalid date format
```json
"tournament_date": "01/15/2026"  // US format
```

✅ **Correct:**
```json
"tournament_date": "2026-01-15"  // ISO format (YYYY-MM-DD)
```

---

❌ **Wrong:** Invalid color code
```json
"color_identity": "Blue-White"  // Full names
```

✅ **Correct:**
```json
"color_identity": "WU"  // Single-letter codes
```

---

❌ **Wrong:** Trailing comma
```json
"games": [
  {"game_number": 1, "winner_name": "Alice"},  // Valid
  {"game_number": 2, "winner_name": "Bob"},    // Invalid trailing comma
]
```

✅ **Correct:**
```json
"games": [
  {"game_number": 1, "winner_name": "Alice"},
  {"game_number": 2, "winner_name": "Bob"}
]
```

## Validation Checklist

Before uploading, verify:
- [ ] JSON syntax is valid (no missing commas, brackets)
- [ ] season_id exists in database
- [ ] Date in YYYY-MM-DD format
- [ ] All player names in matches exist in players array
- [ ] All deck names in matches exist in decks array
- [ ] Color codes use single letters (W, U, B, R, G)
- [ ] Archetype type is one of: Aggro, Control, Combo, Midrange, Other
- [ ] Game numbers are 1, 2, or 3
- [ ] Winner names match player1_name or player2_name
- [ ] No duplicate game numbers within a match

## Tips

💡 Use a JSON validator: https://jsonlint.com/  
💡 Copy `tournament_import_template.json` as starting point  
💡 Reference `tournament_import_example.json` for complete example  
💡 Test with small tournaments first (2-3 matches)  
💡 Save your work frequently  

---

**Files:** `imports/tournament_import_template.json`, `imports/tournament_import_example.json`  
**Upload:** System Manager → "📤 Import" tab  
**Raw Sample:** `imports/DataImport/ForTheChildrenShowdown.json`  
**Clean Sample:** `imports/DataImport/ForTheChildrenShowdown_import.json`
