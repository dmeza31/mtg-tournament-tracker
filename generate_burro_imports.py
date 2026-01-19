import json
from datetime import datetime
from pathlib import Path

def parse_result_string(result_string):
    """Parse result string to extract game wins for each player."""
    # Examples: "Mao88 won 2-1-0", "1-1-0 Draw", "BlackWaldo won 2-0-0"
    if "Draw" in result_string:
        parts = result_string.split()
        scores = parts[0].split('-')
        return int(scores[0]), int(scores[1])
    elif " won " in result_string:
        parts = result_string.split(" won ")
        scores = parts[1].split('-')
        return int(scores[0]), int(scores[1])
    return 0, 0

def extract_tournament_date(date_str):
    """Extract date from DateCreated field."""
    # Format: "2025-12-01T23:43:12Z"
    dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
    return dt.strftime('%Y-%m-%d')

def extract_tournament_name(filename, date_str):
    """Generate tournament name from filename pattern."""
    # Extract month and year from filename
    parts = filename.replace('_', ' ').replace('.json', '').split()
    
    # Determine tournament location/prefix
    if 'OG' in filename or 'og' in parts:
        location_prefix = 'OG'
    elif 'BurroSingle' in filename or 'BurroSingles' in filename:
        location_prefix = 'BurroSingles'
    else:
        location_prefix = 'Unknown'
    
    if 'Diciembre' in parts or 'diciembre' in parts:
        month = 'Diciembre'
    elif 'Noviembre' in parts or 'noviembre' in parts:
        month = 'Noviembre'
    elif 'enero' in parts or 'Enero' in parts:
        month = 'Enero'
    else:
        month = 'Unknown'
    
    # Extract year
    year = None
    for part in parts:
        if part.isdigit() and len(part) == 4:
            year = part
            break
    
    if not year:
        # Try to extract from date_str
        dt = datetime.fromisoformat(date_str.replace('Z', '+00:00'))
        year = str(dt.year)
    
    return f"{location_prefix} Monthly {month} {year}"

def process_tournament_file(input_file, season_id):
    """Process a tournament JSON file and generate import format."""
    
    with open(input_file, 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    matches = data['Content']
    total_records = data.get('RecordsFiltered', len(matches))
    
    if not matches:
        print(f"No matches found in {input_file}")
        return None
    
    print(f"  Total records in source: {total_records}")
    
    # Extract tournament info from first match
    first_match = matches[0]
    date_created = first_match['DateCreated']
    tournament_date = extract_tournament_date(date_created)
    tournament_name = extract_tournament_name(Path(input_file).name, date_created)
    
    # Extract unique players with their decklists
    players_dict = {}
    decks_set = set()
    player_deck_map = {}  # Map player ID to deck name
    
    for match in matches:
        for competitor in match['Competitors']:
            team = competitor['Team']
            for player in team['Players']:
                player_id = player['ID']
                player_name = player['Name']
                player_email = player['Username'].lower() + '@email.com'
                
                if player_id not in players_dict:
                    players_dict[player_id] = {
                        'name': player_name,
                        'email': player_email
                    }
                
                # Extract deck info
                if competitor['Decklists']:
                    for decklist in competitor['Decklists']:
                        deck_name = decklist['DecklistName']
                        decks_set.add(deck_name)
                        player_deck_map[player_id] = deck_name
    
    # Convert to lists
    players = list(players_dict.values())
    decks = [{'name': deck_name, 'color_identity': 'Unknown', 'archetype_type': 'Other'} 
             for deck_name in sorted(decks_set)]
    
    # Check if any player doesn't have a deck mapped - if so, add "Unknown" deck
    has_unknown = any(player_id not in player_deck_map for player_id in players_dict.keys())
    if has_unknown and 'Unknown' not in decks_set:
        decks.append({'name': 'Unknown', 'color_identity': 'Unknown', 'archetype_type': 'Other'})
    
    # Process matches
    matches_output = []
    skipped_byes = 0
    skipped_incomplete = 0
    skipped_no_competitors = 0
    
    for match in matches:
        if len(match['Competitors']) != 2:
            skipped_no_competitors += 1
            continue
        
        competitor1 = match['Competitors'][0]
        competitor2 = match['Competitors'][1]
        
        player1 = competitor1['Team']['Players'][0]
        player2 = competitor2['Team']['Players'][0]
        
        player1_name = player1['Name']
        player2_name = player2['Name']
        player1_id = player1['ID']
        player2_id = player2['ID']
        
        # Get deck names
        player1_deck_name = player_deck_map.get(player1_id, 'Unknown')
        player2_deck_name = player_deck_map.get(player2_id, 'Unknown')
        
        # Parse result
        result_string = match.get('ResultString', '')
        if not result_string or 'bye' in result_string.lower():
            skipped_byes += 1
            continue
        
        def safe_win_count(competitor):
            """Prefer explicit game wins from the export; fallback to zero."""
            wins = competitor.get('GameWinsAndGameByes')
            if wins is None:
                wins = competitor.get('GameWins')
            return int(wins) if wins is not None else 0

        player1_wins = safe_win_count(competitor1)
        player2_wins = safe_win_count(competitor2)

        # If export lacks win counts, fall back to parsing the result string
        if (player1_wins + player2_wins) == 0:
            player1_wins, player2_wins = parse_result_string(result_string)
        
        # Create games array
        games = []
        
        # Distribute wins to games
        for i in range(player1_wins):
            games.append({
                'game_number': i + 1,
                'winner_name': player1_name
            })
        
        for i in range(player2_wins):
            games.append({
                'game_number': player1_wins + i + 1,
                'winner_name': player2_name
            })
        
        # Only add matches with at least 2 games (valid matches)
        if len(games) >= 2:
            match_output = {
                'round_number': match['RoundNumber'],
                'player1_name': player1_name,
                'player2_name': player2_name,
                'player1_deck_name': player1_deck_name,
                'player2_deck_name': player2_deck_name,
                'games': games
            }
            
            matches_output.append(match_output)
        else:
            skipped_incomplete += 1
    
    print(f"  Skipped (not 2 competitors): {skipped_no_competitors}")
    print(f"  Skipped byes: {skipped_byes}")
    print(f"  Skipped incomplete matches (< 2 games): {skipped_incomplete}")
    print(f"  Valid matches: {len(matches_output)}")
    
    # Build final output
    output = {
        'season_id': season_id,
        'tournament': {
            'name': tournament_name,
            'tournament_date': tournament_date,
            'location': 'Burro Singles',
            'format': 'Premodern',
            'tournament_type_name': 'LGS Tournament',
            'description': f'{tournament_name} - Premodern Tournament'
        },
        'players': players,
        'decks': decks,
        'matches': matches_output
    }
    
    return output

def main():
    # Define input files and their season IDs
    files_to_process = [
        {
            'input': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingle_Monthly_Diciembre_2025.json',
            'output': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingle_Monthly_Diciembre_2025_import.json',
            'season_id': 1
        },
        {
            'input': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingles_Monthly_Noviembre_2025.json',
            'output': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingles_Monthly_Noviembre_2025_import.json',
            'season_id': 1
        },
        {
            'input': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingles_monthy_enero_2026.json',
            'output': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\BurroSingles_monthy_enero_2026_import.json',
            'season_id': 2
        },
        {
            'input': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\OG_monthly_noviembre_2025.json',
            'output': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\OG_monthly_noviembre_2025_import.json',
            'season_id': 1
        },
        {
            'input': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\OG_Monthly_Diciembre_2025.json',
            'output': r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\OG_Monthly_Diciembre_2025_import.json',
            'season_id': 1
        }
    ]
    
    created_files = []
    
    for file_info in files_to_process:
        print(f"\nProcessing {Path(file_info['input']).name}...")
        
        try:
            result = process_tournament_file(file_info['input'], file_info['season_id'])
            
            if result:
                # Write output file
                with open(file_info['output'], 'w', encoding='utf-8') as f:
                    json.dump(result, f, indent=2, ensure_ascii=False)
                
                created_files.append(file_info['output'])
                print(f"✓ Created: {file_info['output']}")
                print(f"  - Players: {len(result['players'])}")
                print(f"  - Decks: {len(result['decks'])}")
                print(f"  - Matches: {len(result['matches'])}")
            else:
                print(f"✗ Failed to process {file_info['input']}")
        
        except Exception as e:
            print(f"✗ Error processing {file_info['input']}: {str(e)}")
    
    print(f"\n{'='*60}")
    print(f"Import generation complete!")
    print(f"{'='*60}")
    print(f"Created {len(created_files)} import files:")
    for file_path in created_files:
        print(f"  - {file_path}")

if __name__ == '__main__':
    main()
