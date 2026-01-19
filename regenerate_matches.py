#!/usr/bin/env python3
"""
Script to parse tournament JSON and generate a properly formatted import file
with all matches and game information extracted from the raw tournament data.

Usage:
    python regenerate_matches.py <input_file> [output_file]
    
Example:
    python regenerate_matches.py imports/DataImport/ForTheChildrenShowdown.json
    python regenerate_matches.py imports/DataImport/ForTheChildrenShowdown.json imports/DataImport/ForTheChildrenShowdown_import.json
"""

import json
import re
import sys
import os

# Parse command line arguments
if len(sys.argv) < 2:
    print(__doc__)
    print("Error: Input file is required")
    sys.exit(1)

input_file = sys.argv[1]

# Determine output file (defaults to same name with _import suffix)
if len(sys.argv) >= 3:
    output_file = sys.argv[2]
else:
    base = os.path.splitext(input_file)[0]
    output_file = f"{base}_import.json"

print(f"Input file:  {input_file}")
print(f"Output file: {output_file}")
print()

if not os.path.exists(input_file):
    print(f"Error: Input file not found: {input_file}")
    sys.exit(1)

print("Reading raw tournament data...")
with open(input_file, "r", encoding="utf-8") as f:
    raw_data = json.load(f)

if os.path.exists(output_file):
    print(f"Reading existing players and decks from {output_file}...")
    with open(output_file, "r", encoding="utf-8") as f:
        current_import = json.load(f)
else:
    print(f"Warning: {output_file} not found, will need to create players/decks")
    current_import = {"season_id": 1, "tournament": {}, "players": [], "decks": []}

print("Extracting matches from tournament data...")
matches = []

for match_record in raw_data.get("Content", []):
    round_num = match_record.get("RoundNumber")
    result_str = match_record.get("ResultString", "")

    competitors = match_record.get("Competitors", [])
    if len(competitors) < 2:
        continue

    p1_info = competitors[0]
    p2_info = competitors[1]

    p1_name = p1_info.get("Team", {}).get("Players", [{}])[0].get("Name", "Unknown")
    p2_name = p2_info.get("Team", {}).get("Players", [{}])[0].get("Name", "Unknown")

    p1_deck = p1_info.get("Decklists", [{}])[0].get("DecklistName", "Unknown")
    p2_deck = p2_info.get("Decklists", [{}])[0].get("DecklistName", "Unknown")

    p1_wins = p1_info.get("GameWins") or 0
    p2_wins = p2_info.get("GameWins") or 0

    games_list = []

    if "1-1-0 Draw" in result_str or "Draw" in result_str:
        games_list = [
            {"game_number": 1, "winner_name": p1_name},
            {"game_number": 2, "winner_name": p2_name},
            {"game_number": 3, "winner_name": "Draw"}
        ]
    elif p1_name in result_str and "won" in result_str:
        match = re.search(r"(\d+)-(\d+)-(\d+)", result_str)
        if match:
            p1_game_wins, p2_game_wins, _ = int(match.group(1)), int(match.group(2)), int(match.group(3))
            for g in range(1, p1_game_wins + 1):
                games_list.append({"game_number": g, "winner_name": p1_name})
            for g in range(p1_game_wins + 1, p1_game_wins + p2_game_wins + 1):
                games_list.append({"game_number": g, "winner_name": p2_name})
    elif p2_name in result_str and "won" in result_str:
        match = re.search(r"(\d+)-(\d+)-(\d+)", result_str)
        if match:
            p2_game_wins, p1_game_wins, _ = int(match.group(1)), int(match.group(2)), int(match.group(3))
            for g in range(1, p2_game_wins + 1):
                games_list.append({"game_number": g, "winner_name": p2_name})
            for g in range(p2_game_wins + 1, p2_game_wins + p1_game_wins + 1):
                games_list.append({"game_number": g, "winner_name": p1_name})

    if len(games_list) < 2:
        if p1_wins >= p2_wins:
            for i in range(p1_wins):
                games_list.append({"game_number": i + 1, "winner_name": p1_name})
            for i in range(p2_wins):
                games_list.append({"game_number": len(games_list) + 1, "winner_name": p2_name})
        else:
            for i in range(p2_wins):
                games_list.append({"game_number": i + 1, "winner_name": p2_name})
            for i in range(p1_wins):
                games_list.append({"game_number": len(games_list) + 1, "winner_name": p1_name})

    if len(games_list) < 2:
        if len(games_list) == 1:
            games_list.append({"game_number": 2, "winner_name": p1_name})
        else:
            games_list = [
                {"game_number": 1, "winner_name": p1_name},
                {"game_number": 2, "winner_name": p2_name}
            ]

    if len(games_list) > 3:
        games_list = games_list[:3]

    for game in games_list:
        if "duration_minutes" not in game:
            game["duration_minutes"] = 15

    match_obj = {
        "round_number": round_num,
        "player1_name": p1_name,
        "player2_name": p2_name,
        "player1_deck_name": p1_deck,
        "player2_deck_name": p2_deck,
        "games": games_list
    }

    matches.append(match_obj)

print(f"Extracted {len(matches)} matches")

import_data = {
    "season_id": current_import["season_id"],
    "tournament": current_import["tournament"],
    "players": current_import["players"],
    "decks": current_import["decks"],
    "matches": matches
}

with open(output_file, "w", encoding="utf-8") as f:
    json.dump(import_data, f, indent=2, ensure_ascii=False)

print(f"✓ Updated {output_file} with {len(matches)} properly formatted matches")
print("\nSample matches:")
for i, match in enumerate(matches[:3]):
    print(f"  Match {i + 1}: Round {match['round_number']} - {match['player1_name']} vs {match['player2_name']} ({len(match['games'])} games)")
