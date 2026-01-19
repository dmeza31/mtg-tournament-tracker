"""
MTG Tournament Tracker - System Manager (CRUD Management Dashboard)
Provides UI for managing seasons, tournaments, and matches via API CRUD operations.
Supports local development and Railway deployment with unified configuration.
"""

import os
import streamlit as st
import requests
import pandas as pd
from typing import List, Dict, Optional
from datetime import datetime
import json

# ============================================================================
# Configuration - Works in both local and Railway environments
# ============================================================================
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Initialize session state
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Page configuration
st.set_page_config(
    page_title="MTG Tournament Tracker - System Manager",
    page_icon="⚙️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #2c3e50;
        text-align: center;
        margin-bottom: 2rem;
    }
    .success-box {
        background-color: #d4edda;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #28a745;
        margin-bottom: 1rem;
    }
    .error-box {
        background-color: #f8d7da;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #dc3545;
        margin-bottom: 1rem;
    }
    .info-box {
        background-color: #d1ecf1;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #17a2b8;
        margin-bottom: 1rem;
    }
    </style>
""", unsafe_allow_html=True)

# ============================================================================
# Utility Functions
# ============================================================================

def make_request(method: str, endpoint: str, data: Optional[Dict] = None, use_api_prefix: bool = True) -> tuple[bool, Dict]:
    """Make API request and return (success, response_data)"""
    try:
        if use_api_prefix:
            url = f"{API_BASE_URL}/{endpoint}"
        else:
            # For root-level endpoints like /health
            base = API_BASE_URL.replace("/api/v1", "")
            url = f"{base}/{endpoint}"
        headers = {"Content-Type": "application/json"}
        
        if method.upper() == "GET":
            response = requests.get(url, headers=headers, params=data)
        elif method.upper() == "POST":
            response = requests.post(url, json=data, headers=headers)
        elif method.upper() == "PUT":
            response = requests.put(url, json=data, headers=headers)
        elif method.upper() == "DELETE":
            response = requests.delete(url, headers=headers)
        else:
            return False, {"error": f"Unknown method: {method}"}
        
        if response.status_code in [200, 201]:
            return True, response.json()
        else:
            return False, {"error": response.text, "status_code": response.status_code}
    except Exception as e:
        return False, {"error": str(e)}

# ============================================================================
# SEASON TAB
# ============================================================================

def render_season_tab():
    st.header("📅 Season Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search & Update Existing Season")
        season_search = st.text_input("Search by season name (partial match):", key="season_search")
        
        if season_search:
            success, data = make_request("GET", "seasons")
            if success:
                seasons = data if isinstance(data, list) else data.get('data', [])
                filtered = [s for s in seasons if season_search.lower() in str(s.get('name', '')).lower()]
                
                if filtered:
                    season_options = {f"{s['id']}: {s['name']}": s for s in filtered}
                    selected = st.selectbox("Select season:", options=list(season_options.keys()))
                    
                    if selected:
                        season = season_options[selected]
                        st.write("**Current Details:**")
                        st.json(season)
                        
                        with st.form("update_season_form"):
                            st.subheader("Update Season")
                            new_name = st.text_input("Season Name:", value=season.get('name', ''))
                            new_start_date = st.date_input("Start Date:", value=datetime.strptime(season.get('start_date', '2025-01-01'), '%Y-%m-%d').date() if season.get('start_date') else datetime.now().date())
                            new_end_date = st.date_input("End Date:", value=datetime.strptime(season.get('end_date', '2025-12-31'), '%Y-%m-%d').date() if season.get('end_date') else datetime.now().date())
                            new_description = st.text_area("Description:", value=season.get('description', ''), height=100)
                            
                            if st.form_submit_button("Update Season"):
                                update_data = {
                                    "name": new_name,
                                    "start_date": new_start_date.isoformat(),
                                    "end_date": new_end_date.isoformat(),
                                    "description": new_description
                                }
                                success, response = make_request("PUT", f"seasons/{season['id']}", update_data)
                                if success:
                                    st.markdown(f"<div class='success-box'>✅ Season updated successfully!</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)
                else:
                    st.info("No seasons found matching that name.")
        else:
            st.info("Enter a season name to search.")
    
    with col2:
        st.subheader("Create New Season")
        with st.form("create_season_form"):
            season_name = st.text_input("Season Name:")
            season_start = st.date_input("Start Date:")
            season_end = st.date_input("End Date:")
            season_description = st.text_area("Description:", height=100)
            
            if st.form_submit_button("Create Season"):
                create_data = {
                    "name": season_name,
                    "start_date": season_start.isoformat(),
                    "end_date": season_end.isoformat(),
                    "description": season_description
                }
                success, response = make_request("POST", "seasons", create_data)
                if success:
                    st.markdown(f"<div class='success-box'>✅ Season created successfully! ID: {response.get('id')}</div>", unsafe_allow_html=True)
                else:
                    st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)

# ============================================================================
# TOURNAMENT TAB
# ============================================================================

def render_tournament_tab():
    st.header("🏆 Tournament Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search & Update Existing Tournament")
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            # Fetch tournaments once for dropdown search
            all_tournaments_success, all_tournaments_data = make_request("GET", "tournaments")
            all_tournaments = all_tournaments_data if all_tournaments_success and isinstance(all_tournaments_data, list) else all_tournaments_data.get('data', []) if all_tournaments_success else []
            tournament_name_options = ["(Any)"] + [f"{t['id']}: {t['name']}" for t in all_tournaments]
            tournament_name_selected = st.selectbox("Search by tournament name:", options=tournament_name_options, key="tournament_name_search_select")
            tournament_name_search = None if tournament_name_selected == "(Any)" else tournament_name_selected.split(": ",1)[1]
        with search_col2:
            tournament_location_search = st.text_input("Search by location (partial):", key="tournament_location_search")
        
        if tournament_name_search or tournament_location_search:
            tournaments = all_tournaments
            if tournaments:
                filtered = tournaments
                
                if tournament_name_search:
                    filtered = [t for t in filtered if tournament_name_search.lower() in str(t.get('name', '')).lower()]
                if tournament_location_search:
                    filtered = [t for t in filtered if tournament_location_search.lower() in str(t.get('location', '')).lower()]
                
                if filtered:
                    tournament_options = {f"{t['id']}: {t['name']} ({t.get('location', 'N/A')})": t for t in filtered}
                    selected = st.selectbox("Select tournament:", options=list(tournament_options.keys()))
                    
                    if selected:
                        tournament = tournament_options[selected]
                        st.write("**Current Details:**")
                        st.json(tournament)
                        
                        with st.form("update_tournament_form"):
                            st.subheader("Update Tournament")
                            new_name = st.text_input("Tournament Name:", value=tournament.get('name', ''))
                            new_location = st.text_input("Location:", value=tournament.get('location', ''))
                            new_format = st.text_input("Format:", value=tournament.get('format', ''))
                            new_date = st.date_input("Date:", value=datetime.strptime(tournament.get('tournament_date', '2025-01-01'), '%Y-%m-%d').date() if tournament.get('tournament_date') else datetime.now().date())
                            
                            # Fetch tournament types from API
                            type_success, type_data = make_request("GET", "tournament-types")
                            tournament_types_list = []
                            if type_success:
                                tournament_types_list = type_data if isinstance(type_data, list) else type_data.get('data', [])
                            
                            # Find current type index
                            current_type_id = tournament.get('tournament_type_id')
                            current_type_index = 0
                            if tournament_types_list and current_type_id:
                                for idx, t in enumerate(tournament_types_list):
                                    if t.get('id') == current_type_id:
                                        current_type_index = idx
                                        break
                            
                            if tournament_types_list:
                                type_options = {f"{t['id']}: {t['name']}": t['id'] for t in tournament_types_list}
                                selected_type = st.selectbox("Type:", options=list(type_options.keys()), index=current_type_index, key="update_tournament_type_select")
                                new_type_id = type_options[selected_type] if selected_type else None
                            else:
                                st.warning("No tournament types available.")
                                new_type_id = current_type_id
                            
                            new_description = st.text_area("Description:", value=tournament.get('description', ''), height=100)
                            
                            if st.form_submit_button("Update Tournament"):
                                update_data = {
                                    "name": new_name,
                                    "location": new_location,
                                    "format": new_format,
                                    "tournament_date": new_date.isoformat(),
                                    "tournament_type_id": new_type_id,
                                    "description": new_description
                                }
                                success, response = make_request("PUT", f"tournaments/{tournament['id']}", update_data)
                                if success:
                                    st.markdown(f"<div class='success-box'>✅ Tournament updated successfully!</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)
                else:
                    st.info("No tournaments found matching those criteria.")
        else:
            st.info("Enter a tournament name or location to search.")
    
    with col2:
        st.subheader("Create New Tournament")
        with st.form("create_tournament_form"):
            # Fetch seasons for dropdown
            season_success, season_data = make_request("GET", "seasons")
            seasons = []
            if season_success:
                seasons = season_data if isinstance(season_data, list) else season_data.get('data', [])
            
            season_options = {f"{s['id']}: {s['name']}": s['id'] for s in seasons}
            selected_season = st.selectbox("Select Season:", options=list(season_options.keys()), key="tournament_season_select")
            season_id = season_options[selected_season] if selected_season else None
            
            tournament_name = st.text_input("Tournament Name:")
            tournament_location = st.text_input("Location:")
            tournament_format = st.text_input("Format (e.g., Standard, Modern):")
            
            # Fetch tournament types from API
            type_success, type_data = make_request("GET", "tournament-types")
            tournament_types_list = []
            if type_success:
                tournament_types_list = type_data if isinstance(type_data, list) else type_data.get('data', [])
            
            if tournament_types_list:
                type_options = {f"{t['id']}: {t['name']}": t['id'] for t in tournament_types_list}
                selected_type = st.selectbox("Type:", options=list(type_options.keys()), key="create_tournament_type_select")
                tournament_type_id = type_options[selected_type] if selected_type else None
            else:
                st.warning("No tournament types available. Please create one in the Tournament Types tab first.")
                tournament_type_id = None
            
            tournament_description = st.text_area("Description:", height=100)
            tournament_date = st.date_input("Tournament Date:")
            
            if st.form_submit_button("Create Tournament"):
                if not season_id:
                    st.error("Please select a season.")
                elif not tournament_type_id:
                    st.error("Please select a tournament type.")
                else:
                    create_data = {
                        "season_id": season_id,
                        "name": tournament_name,
                        "location": tournament_location,
                        "format": tournament_format,
                        "tournament_type_id": tournament_type_id,
                        "description": tournament_description,
                        "tournament_date": tournament_date.isoformat()
                    }
                    success, response = make_request("POST", "tournaments", create_data)
                    if success:
                        st.markdown(f"<div class='success-box'>✅ Tournament created successfully! ID: {response.get('id')}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)

# ============================================================================
# MATCH TAB
# ============================================================================

def render_match_tab():
    st.header("🎮 Match Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search & Update Existing Match")
        search_col1, search_col2 = st.columns(2)
        with search_col1:
            # Fetch tournaments for dropdown filter
            t_success, t_data = make_request("GET", "tournaments")
            tournaments_for_filter = t_data if t_success and isinstance(t_data, list) else t_data.get('data', []) if t_success else []
            t_options = ["(Any)"] + [f"{t['id']}: {t['name']}" for t in tournaments_for_filter]
            tournament_filter_selected = st.selectbox("Filter by tournament name:", options=t_options, key="match_tournament_filter_select")
            tournament_filter = None if tournament_filter_selected == "(Any)" else tournament_filter_selected.split(": ",1)[1]
        with search_col2:
            player_filter = st.text_input("Filter by player name:", key="match_player_filter")
        
        if tournament_filter or player_filter:
            success, data = make_request("GET", "matches")
            if success:
                matches = data if isinstance(data, list) else data.get('data', [])
                filtered = matches
                
                if tournament_filter:
                    # Need to get tournament names - simplified for now
                    filtered = [m for m in filtered if tournament_filter.lower() in str(m).lower()]
                if player_filter:
                    filtered = [m for m in filtered if player_filter.lower() in str(m.get('player1_name', '')).lower() or player_filter.lower() in str(m.get('player2_name', '')).lower()]
                
                if filtered:
                    match_options = {f"{m['id']}: {m.get('player1_name', 'P1')} vs {m.get('player2_name', 'P2')} (R{m.get('round_number', '?')})": m for m in filtered[:20]}
                    selected = st.selectbox("Select match:", options=list(match_options.keys()))
                    
                    if selected:
                        match = match_options[selected]
                        # Fetch full match details (with games)
                        detail_success, match_detail = make_request("GET", f"matches/{match['id']}")
                        if not detail_success:
                            st.markdown(f"<div class='error-box'>❌ Error fetching match details: {match_detail.get('error')}</div>", unsafe_allow_html=True)
                            return
                        st.write("**Current Details:**")
                        st.json(match_detail)
                        
                        # Fetch players for dropdowns
                        player_success, player_data = make_request("GET", "players")
                        players_list = player_data if player_success and isinstance(player_data, list) else player_data.get('data', []) if player_success else []
                        player_options = {f"{p['id']}: {p['name']}": p['id'] for p in players_list}
                        player_name_lookup = {p['id']: p['name'] for p in players_list}
                        if not player_options:
                            st.warning("No players available to update this match.")
                            return
                        
                        with st.form("update_match_form"):
                            st.subheader("Update Match")
                            p1_default = next((k for k,v in player_options.items() if v == match_detail.get('player1_id')), None)
                            p2_default = next((k for k,v in player_options.items() if v == match_detail.get('player2_id')), None)
                            selected_p1 = st.selectbox("Player 1:", options=list(player_options.keys()), index=list(player_options.keys()).index(p1_default) if p1_default else 0)
                            selected_p2 = st.selectbox("Player 2:", options=list(player_options.keys()), index=list(player_options.keys()).index(p2_default) if p2_default else 0)
                            new_round = st.number_input("Round Number:", value=match_detail.get('round_number', 1), min_value=1)
                            
                            if st.form_submit_button("Update Match"):
                                update_data = {
                                    "player1_id": player_options[selected_p1],
                                    "player2_id": player_options[selected_p2],
                                    "round_number": new_round
                                }
                                success, response = make_request("PUT", f"matches/{match['id']}", update_data)
                                if success:
                                    st.markdown(f"<div class='success-box'>✅ Match updated successfully!</div>", unsafe_allow_html=True)
                                else:
                                    st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)
                        
                        # Games editing
                        st.subheader("Update Games")
                        games = match_detail.get('games', [])

                        # Winner options (shared)
                        winner_options = {}
                        if match_detail.get('player1_id'):
                            winner_options[player_name_lookup.get(match_detail['player1_id'], 'Player 1')] = match_detail['player1_id']
                        if match_detail.get('player2_id'):
                            winner_options[player_name_lookup.get(match_detail['player2_id'], 'Player 2')] = match_detail['player2_id']

                        if games:
                            for game in games:
                                st.markdown(f"**Game {game.get('game_number')} (ID: {game.get('id')})**")
                                with st.form(f"update_game_{game.get('id')}"):
                                    current_winner = next((label for label, pid in winner_options.items() if pid == game.get('winner_id')), None)
                                    selected_winner = st.selectbox("Winner:", options=list(winner_options.keys()), index=list(winner_options.keys()).index(current_winner) if current_winner else 0)
                                    selected_result = st.selectbox("Game Result:", options=["WIN", "DRAW"], index=["WIN", "DRAW"].index(game.get('game_result', 'WIN')) if game.get('game_result') in ["WIN", "DRAW"] else 0)
                                    if st.form_submit_button("Update Game"):
                                        update_game_payload = {
                                            "winner_id": winner_options[selected_winner],
                                            "game_result": selected_result
                                        }
                                        g_success, g_response = make_request("PUT", f"matches/{match['id']}/games/{game.get('id')}", update_game_payload)
                                        if g_success:
                                            st.markdown(f"<div class='success-box'>✅ Game updated successfully!</div>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<div class='error-box'>❌ Error: {g_response.get('error')}</div>", unsafe_allow_html=True)
                        else:
                            st.info("No games found for this match.")

                        # Add game (if slots remain)
                        existing_numbers = {g.get('game_number') for g in games if g.get('game_number') is not None}
                        available_numbers = [n for n in [1, 2, 3] if n not in existing_numbers]
                        if available_numbers:
                            st.subheader("Add Game")
                            with st.form(f"add_game_{match['id']}"):
                                next_game_default = min(available_numbers)
                                game_number = st.selectbox("Game Number:", options=available_numbers, index=available_numbers.index(next_game_default))
                                selected_winner_label = st.selectbox("Winner:", options=list(winner_options.keys()) if winner_options else [])
                                selected_result = st.selectbox("Game Result:", options=["WIN", "DRAW"], index=0)
                                duration = st.number_input("Duration (minutes):", min_value=1, value=10)
                                notes = st.text_area("Notes (optional):", height=60)
                                if st.form_submit_button("Add Game"):
                                    if not winner_options:
                                        st.error("No players available to assign as winner.")
                                    else:
                                        payload = {
                                            "game_number": game_number,
                                            "winner_id": winner_options[selected_winner_label],
                                            "game_result": selected_result,
                                            "duration_minutes": duration,
                                            "notes": notes
                                        }
                                        create_success, create_resp = make_request("POST", f"matches/{match['id']}/games", payload)
                                        if create_success:
                                            st.markdown(f"<div class='success-box'>✅ Game added successfully!</div>", unsafe_allow_html=True)
                                        else:
                                            st.markdown(f"<div class='error-box'>❌ Error: {create_resp.get('error')}</div>", unsafe_allow_html=True)
                        else:
                            st.info("All 3 games already exist for this match.")
                else:
                    st.info("No matches found matching those criteria.")
        else:
            st.info("Enter a tournament name or player name to search.")
    
    with col2:
        st.subheader("Create New Match")
        with st.form("create_match_form"):
            # Fetch tournaments for dropdown
            tournament_success, tournament_data = make_request("GET", "tournaments")
            tournaments = []
            if tournament_success:
                tournaments = tournament_data if isinstance(tournament_data, list) else tournament_data.get('data', [])
            
            tournament_options = {f"{t['id']}: {t['name']}": t['id'] for t in tournaments}
            selected_tournament = st.selectbox("Select Tournament:", options=list(tournament_options.keys()), key="match_tournament_select")
            tournament_id = tournament_options[selected_tournament] if selected_tournament else None
            
            # Fetch players for dropdown
            player_success, player_data = make_request("GET", "players")
            players = []
            if player_success:
                players = player_data if isinstance(player_data, list) else player_data.get('data', [])
            
            player_options = {f"{p['id']}: {p['name']}": p['id'] for p in players}
            
            col_p1, col_p2 = st.columns(2)
            with col_p1:
                selected_p1 = st.selectbox("Player 1:", options=list(player_options.keys()), key="match_p1_select")
                p1_id = player_options[selected_p1] if selected_p1 else None
            with col_p2:
                selected_p2 = st.selectbox("Player 2:", options=list(player_options.keys()), key="match_p2_select")
                p2_id = player_options[selected_p2] if selected_p2 else None
            
            round_num = st.number_input("Round Number:", value=1, min_value=1)
            
            if st.form_submit_button("Create Match"):
                if not all([tournament_id, p1_id, p2_id]):
                    st.error("Please select tournament and both players.")
                else:
                    create_data = {
                        "tournament_id": tournament_id,
                        "player1_id": p1_id,
                        "player2_id": p2_id,
                        "round_number": round_num
                    }
                    success, response = make_request("POST", "matches", create_data)
                    if success:
                        st.markdown(f"<div class='success-box'>✅ Match created successfully! ID: {response.get('id')}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)

# ============================================================================
# IMPORT TAB
# ============================================================================

def render_import_tab():
    st.header("📤 Tournament Import")
    st.markdown("Upload a JSON file to import a full tournament (tournament, players, decks, matches, games) through the API in one step.")
    st.info("Use the templates in imports/ (template and example) to build your JSON. Missing tournament type defaults to 'LGS Tournament'.")

    uploaded_file = st.file_uploader("Upload tournament JSON:", type=["json"], help="Upload a single tournament JSON file")

    if uploaded_file is not None:
        try:
            file_contents = uploaded_file.read()
            tournament_data = json.loads(file_contents)

            # Default tournament type when not provided
            if isinstance(tournament_data, dict):
                tournament_section = tournament_data.get("tournament", {}) or {}
                if (
                    isinstance(tournament_section, dict)
                    and not tournament_section.get("tournament_type_id")
                    and not tournament_section.get("tournament_type_name")
                ):
                    tournament_section["tournament_type_name"] = "LGS Tournament"
                    tournament_data["tournament"] = tournament_section

            st.success("File loaded. Review the preview below before importing.")

            with st.expander("Preview and counts", expanded=True):
                st.json(tournament_data)

                col1, col2, col3, col4 = st.columns(4)
                with col1:
                    st.metric("Players", len(tournament_data.get("players", [])))
                with col2:
                    st.metric("Decks", len(tournament_data.get("decks", [])))
                with col3:
                    st.metric("Matches", len(tournament_data.get("matches", [])))
                with col4:
                    total_games = sum(len(m.get("games", [])) for m in tournament_data.get("matches", []))
                    st.metric("Games", total_games)

            if st.button("🚀 Import Tournament", type="primary", use_container_width=True):
                with st.spinner("Importing tournament..."):
                    success, response = make_request("POST", "tournaments/import-complete", tournament_data)
                    if success:
                        st.markdown(f"<div class='success-box'>✅ Tournament imported successfully!</div>", unsafe_allow_html=True)
                        col1, col2, col3, col4, col5 = st.columns(5)
                        with col1:
                            st.metric("Tournament", "Created" if response.get("tournament_created") else "Exists")
                        with col2:
                            st.metric("Players", response.get("players_created", 0))
                        with col3:
                            st.metric("Decks", response.get("decks_created", 0))
                        with col4:
                            st.metric("Matches", response.get("matches_created", 0))
                        with col5:
                            st.metric("Games", response.get("games_created", 0))
                        if response.get("message"):
                            st.info(response["message"])
                    else:
                        st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)
        except json.JSONDecodeError as e:
            st.markdown(f"<div class='error-box'>❌ Invalid JSON: {str(e)}</div>", unsafe_allow_html=True)
        except Exception as e:
            st.markdown(f"<div class='error-box'>❌ Error: {str(e)}</div>", unsafe_allow_html=True)
    else:
        st.info("Upload a JSON file to begin.")

# ============================================================================
# TOURNAMENT TYPE TAB
# ============================================================================

def render_tournament_type_tab():
    st.header("🏷️ Tournament Type Management")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.subheader("Search & Update Existing Tournament Type")
        types_success, types_data = make_request("GET", "tournament-types")
        tournament_types = types_data if types_success and isinstance(types_data, list) else types_data.get('data', []) if types_success else []

        if tournament_types:
            type_options = {f"{t['id']}: {t['name']}": t for t in tournament_types}
            selected = st.selectbox("Select tournament type:", options=list(type_options.keys()), key="type_search_select")
            
            if selected:
                tournament_type = type_options[selected]
                st.write("**Current Details:**")
                st.json(tournament_type)
                
                with st.form("update_tournament_type_form"):
                    st.subheader("Update Tournament Type")
                    new_name = st.text_input("Type Name:", value=tournament_type.get('name', ''))
                    new_points_win = st.number_input("Points for Win:", value=tournament_type.get('points_win', 0), min_value=0)
                    new_points_draw = st.number_input("Points for Draw:", value=tournament_type.get('points_draw', 0), min_value=0)
                    new_description = st.text_area("Description:", value=tournament_type.get('description', ''), height=100)
                    
                    if st.form_submit_button("Update Tournament Type"):
                        update_data = {
                            "name": new_name,
                            "points_win": new_points_win,
                            "points_draw": new_points_draw,
                            "description": new_description
                        }
                        success, response = make_request("PUT", f"tournament-types/{tournament_type['id']}", update_data)
                        if success:
                            st.markdown(f"<div class='success-box'>✅ Tournament type updated successfully!</div>", unsafe_allow_html=True)
                        else:
                            st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)
        else:
            st.info("No tournament types available to update.")
    
    with col2:
        st.subheader("Create New Tournament Type")
        with st.form("create_tournament_type_form"):
            type_name = st.text_input("Type Name:")
            points_win = st.number_input("Points for Win:", value=5, min_value=0)
            points_draw = st.number_input("Points for Draw:", value=2, min_value=0)
            type_description = st.text_area("Description:", height=100)
            
            if st.form_submit_button("Create Tournament Type"):
                if not type_name:
                    st.error("Please enter a tournament type name.")
                else:
                    create_data = {
                        "name": type_name,
                        "points_win": points_win,
                        "points_draw": points_draw,
                        "description": type_description
                    }
                    success, response = make_request("POST", "tournament-types", create_data)
                    if success:
                        st.markdown(f"<div class='success-box'>✅ Tournament type created successfully! ID: {response.get('id')}</div>", unsafe_allow_html=True)
                    else:
                        st.markdown(f"<div class='error-box'>❌ Error: {response.get('error')}</div>", unsafe_allow_html=True)

# ============================================================================
# MAIN APP
# ============================================================================

def main():
    st.markdown("<h1 class='main-header'>⚙️ MTG Tournament Tracker - System Manager</h1>", unsafe_allow_html=True)
    
    # API Status Check
    success, _ = make_request("GET", "health", use_api_prefix=False)
    if not success:
        st.error(f"⚠️ Cannot connect to API at {API_BASE_URL}")
        st.info("Make sure the API backend is running.")
        return
    else:
        st.success(f"✅ Connected to API at {API_BASE_URL}")
    
    # Tabs
    tab1, tab2, tab3, tab4, tab5 = st.tabs(["📅 Seasons", "🏆 Tournaments", "🎮 Matches", "📤 Import", "🏷️ Tournament Types"])
    
    with tab1:
        render_season_tab()
    
    with tab2:
        render_tournament_tab()
    
    with tab3:
        render_match_tab()
    
    with tab4:
        render_import_tab()
    
    with tab5:
        render_tournament_type_tab()
    
    # Sidebar info
    st.sidebar.markdown("---")
    st.sidebar.subheader("Configuration")
    st.sidebar.info(f"**API Base URL:** {API_BASE_URL}")
    st.sidebar.markdown("---")
    st.sidebar.markdown("### About")
    st.sidebar.markdown("""
    This application provides CRUD management for:
    - **Seasons**: Create and manage tournament seasons
    - **Tournaments**: Organize tournaments within seasons
    - **Matches**: Create and track matches between players
    - **Tournament Types**: Define tournament types with point values
    
    All changes are persisted to the PostgreSQL database via the REST API.
    """)

if __name__ == "__main__":
    main()
