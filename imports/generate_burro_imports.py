import json
import argparse
import sys
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

def process_tournament_file(input_file, season_id, tournament_name, location, format_type='Premodern', tournament_type='LGS Tournament'):
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
            'location': location,
            'format': format_type,
            'tournament_type_name': tournament_type,
            'description': f'{tournament_name} - {format_type} Tournament'
        },
        'players': players,
        'decks': decks,
        'matches': matches_output
    }
    
    return output

def main():
    parser = argparse.ArgumentParser(
        description='Generate tournament import file from MTG Melee JSON export',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
Examples:
  python generate_burro_imports.py tournament.json 2 "OG Monthly Enero 2026" "Only Games"
  python generate_burro_imports.py tournament.json 1 "BurroSingles Monthly" "Burro Singles" -o output.json
  python generate_burro_imports.py tournament.json 2 "Tournament Name" "Location" -f Modern -t "Competitive"
        '''
    )
    
    # Required arguments
    parser.add_argument('input_file', help='Path to tournament JSON file from MTG Melee')
    parser.add_argument('season_id', type=int, help='Season ID number')
    parser.add_argument('tournament_name', help='Tournament name (e.g., "OG Monthly Enero 2026")')
    parser.add_argument('location', help='Tournament location (e.g., "Only Games", "Burro Singles")')
    
    # Optional arguments
    parser.add_argument('-o', '--output', help='Output file path (default: auto-generate from input filename)')
    parser.add_argument('-f', '--format', default='Premodern', help='Tournament format (default: Premodern)')
    parser.add_argument('-t', '--tournament-type', default='LGS Tournament', help='Tournament type (default: LGS Tournament)')
    
    args = parser.parse_args()
    
    # Generate output path if not provided
    if args.output:
        output_file = args.output
    else:
        input_path = Path(args.input_file)
        output_file = str(input_path.parent / f"{input_path.stem}_import.json")
    
    print(f"\nProcessing {Path(args.input_file).name}...")
    print(f"  Season ID: {args.season_id}")
    print(f"  Tournament: {args.tournament_name}")
    print(f"  Location: {args.location}")
    print(f"  Format: {args.format}")
    print(f"  Type: {args.tournament_type}")
    
    try:
        result = process_tournament_file(
            args.input_file,
            args.season_id,
            args.tournament_name,
            args.location,
            args.format,
            args.tournament_type
        )
        
        if result:
            # Write output file
            with open(output_file, 'w', encoding='utf-8') as f:
                json.dump(result, f, indent=2, ensure_ascii=False)
            
            print(f"\n✓ Created: {output_file}")
            print(f"  - Players: {len(result['players'])}")
            print(f"  - Decks: {len(result['decks'])}")
            print(f"  - Matches: {len(result['matches'])}")
        else:
            print(f"\n✗ Failed to process {args.input_file}")
            sys.exit(1)
    
    except FileNotFoundError:
        print(f"\n✗ Error: Input file not found: {args.input_file}")
        sys.exit(1)
    except Exception as e:
        print(f"\n✗ Error processing {args.input_file}: {str(e)}")
        sys.exit(1)

if __name__ == '__main__':
    main()
