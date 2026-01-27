import json

# Load source file
with open(r'c:\Users\dmeza\Desktop\Personal Repo\MTG Tournament Tracker\imports\DataImport\OG_Monthly_Enero_2026.json', encoding='utf-8') as f:
    data = json.load(f)

matches = data['Content']

print(f'Total records: {len(matches)}')
print(f'With 2 competitors: {sum(1 for m in matches if len(m["Competitors"]) == 2)}')
print(f'With 1 competitor (byes): {sum(1 for m in matches if len(m["Competitors"]) == 1)}')

print('\n=== Match Details ===')
for m in matches:
    comp_count = len(m["Competitors"])
    game_wins = [c.get("GameWins") or c.get("GameWinsAndGameByes") for c in m["Competitors"]]
    total_games = sum(w for w in game_wins if w is not None)
    
    print(f'Round {m["RoundNumber"]}: {m["ResultString"]}')
    print(f'  Competitors: {comp_count}, GameWins: {game_wins}, Total: {total_games}')
    
    # Check if this would be skipped
    if comp_count != 2:
        print(f'  -> SKIPPED: Not 2 competitors')
    elif total_games < 2:
        print(f'  -> SKIPPED: Less than 2 total games')
    else:
        print(f'  -> INCLUDED')
    print()
