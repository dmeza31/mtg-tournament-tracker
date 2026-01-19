"""
MTG Tournament Tracker - Streamlit Dashboard
Displays season standings, deck statistics, and tournament results with interactive visualizations.
"""

import os
import streamlit as st
import requests
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from typing import List, Dict, Optional
from translations import t, TRANSLATIONS

# Configuration
API_BASE_URL = os.getenv("API_BASE_URL", "http://localhost:8000/api/v1")

# Initialize session state for language
if 'language' not in st.session_state:
    st.session_state.language = 'en'

# Page configuration
st.set_page_config(
    page_title=t('app_title', st.session_state.language),
    page_icon="🎴",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
    <style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #1f77b4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .metric-card {
        background-color: #f0f2f6;
        padding: 1rem;
        border-radius: 0.5rem;
        border-left: 4px solid #1f77b4;
    }
    .standings-table {
        font-size: 0.9rem;
    }
    </style>
""", unsafe_allow_html=True)


# API Functions
@st.cache_data(ttl=60)
def get_seasons() -> List[Dict]:
    """Fetch all seasons from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/seasons")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching seasons: {e}")
        return []


@st.cache_data(ttl=60)
def get_season_standings(season_id: Optional[int] = None) -> List[Dict]:
    """Fetch season standings from API."""
    try:
        if season_id:
            response = requests.get(f"{API_BASE_URL}/stats/season-standings/{season_id}")
        else:
            response = requests.get(f"{API_BASE_URL}/stats/season-standings")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching season standings: {e}")
        return []


@st.cache_data(ttl=60)
def get_deck_statistics() -> List[Dict]:
    """Fetch deck statistics from API."""
    try:
        response = requests.get(f"{API_BASE_URL}/stats/decks")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching deck statistics: {e}")
        return []


@st.cache_data(ttl=60)
def get_tournaments(season_id: Optional[int] = None) -> List[Dict]:
    """Fetch tournaments from API."""
    try:
        if season_id:
            response = requests.get(f"{API_BASE_URL}/tournaments?season_id={season_id}")
        else:
            response = requests.get(f"{API_BASE_URL}/tournaments")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tournaments: {e}")
        return []


@st.cache_data(ttl=60)
def get_tournament_matches(tournament_id: int) -> List[Dict]:
    """Fetch matches for a specific tournament."""
    try:
        response = requests.get(f"{API_BASE_URL}/matches?tournament_id={tournament_id}")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching tournament matches: {e}")
        return []


@st.cache_data(ttl=60)
def get_deck_matchups() -> List[Dict]:
    """Fetch all deck matchup statistics."""
    try:
        response = requests.get(f"{API_BASE_URL}/stats/matchups")
        response.raise_for_status()
        return response.json()
    except requests.exceptions.RequestException as e:
        st.error(f"Error fetching deck matchups: {e}")
        return []


def display_season_standings(standings: List[Dict], season_name: str):
    """Display season standings as a formatted table."""
    lang = st.session_state.language
    
    if not standings:
        st.warning(t('no_standings', lang))
        return
    
    st.subheader(t('standings_title', lang, season=season_name))
    
    # Convert to DataFrame
    df = pd.DataFrame(standings)
    
    # Add position column
    df.insert(0, 'Position', range(1, len(df) + 1))
    
    # Select and rename columns for display
    display_df = df[[
        'Position', 'player_name', 'matches_played', 
        'wins', 'draws', 'losses', 'points'
    ]].copy()
    
    display_df.columns = [
        t('pos', lang), 
        t('player', lang), 
        t('matches_played', lang), 
        t('wins', lang), 
        t('draws', lang), 
        t('losses', lang), 
        t('points', lang)
    ]
    
    # Highlight champion (first place)
    def highlight_champion(row):
        if row[t('pos', lang)] == 1:
            return ['background-color: #FFD700; font-weight: bold'] * len(row)
        elif row[t('pos', lang)] == 2:
            return ['background-color: #C0C0C0'] * len(row)
        elif row[t('pos', lang)] == 3:
            return ['background-color: #CD7F32'] * len(row)
        return [''] * len(row)
    
    styled_df = display_df.style.apply(highlight_champion, axis=1)
    
    st.dataframe(styled_df, use_container_width=True, hide_index=True)
    
    # Explanation of standings calculation
    with st.expander(t('how_calculated', lang)):
        st.markdown(t('calculation_explanation', lang))
    
    # Display champion info
    champion = standings[0]
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric(t('champion', lang), champion['player_name'])
    with col2:
        st.metric(t('points', lang), champion['points'])
    with col3:
        record = f"{champion['wins']}-{champion['draws']}-{champion['losses']}"
        st.metric(t('record', lang), record)


def display_deck_statistics(deck_stats: List[Dict], lang: str = 'en'):
    """Display deck statistics with win rate chart."""
    lang = st.session_state.language
    
    if not deck_stats:
        st.warning(t('no_deck_stats', lang))
        return
    
    st.subheader(t('deck_stats_title', lang))
    
    # Convert to DataFrame
    df = pd.DataFrame(deck_stats)
    
    # Sort by win rate
    df = df.sort_values('win_rate_percentage', ascending=False)
    
    # Create two columns
    col1, col2 = st.columns([2, 1])
    
    with col1:
        # Win Rate Bar Chart
        fig = px.bar(
            df,
            x='deck_name',
            y='win_rate_percentage',
            color='archetype_type',
            title=t('win_rates', lang),
            labels={
                'deck_name': 'Deck',
                'win_rate_percentage': 'Win Rate (%)',
                'archetype_type': 'Archetype'
            },
            text='win_rate_percentage',
            color_discrete_sequence=px.colors.qualitative.Set2
        )
        
        fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
        fig.update_layout(
            xaxis_tickangle=-45,
            height=500,
            showlegend=True,
            hovermode='x unified'
        )
        
        st.plotly_chart(fig, use_container_width=True)
    
    with col2:
        # Deck Stats Summary
        st.markdown(f"### {t('meta_analysis', lang)}")
        
        total_matches = df['total_matches'].sum()
        
        for _, deck in df.head(5).iterrows():
            meta_share = (deck['total_matches'] / total_matches * 100) if total_matches > 0 else 0
            
            with st.container():
                st.markdown(f"**{deck['deck_name']}**")
                st.markdown(f"- Win Rate: {deck['win_rate_percentage']:.1f}%")
                st.markdown(f"- {t('meta_share', lang)}: {meta_share:.1f}%")
                st.markdown(f"- Record: {deck['matches_won']}-{deck['matches_drawn']}-{deck['matches_lost']}")
                st.markdown("---")
    
    # Detailed Table
    with st.expander(f"📋 {t('detailed_stats', lang)}"):
        display_df = df[[
            'deck_name', 'archetype_type', 'color_identity',
            'total_matches', 'matches_won', 'matches_drawn', 'matches_lost',
            'win_rate_percentage', 'unique_players', 'tournaments_played'
        ]].copy()
        
        display_df.columns = [
            t('deck', lang), t('type', lang), t('colors', lang), t('matches', lang), 
            t('wins', lang), t('draws', lang), t('losses', lang),
            t('win_rate_pct', lang), t('players', lang), t('tournaments', lang)
        ]
        
        st.dataframe(display_df, use_container_width=True, hide_index=True)


def display_archetype_distribution(deck_stats: List[Dict], lang: str = 'en'):
    """Display pie chart of archetype distribution."""
    if not deck_stats:
        return
    
    df = pd.DataFrame(deck_stats)
    
    # Group by archetype type
    archetype_counts = df.groupby('archetype_type')['total_matches'].sum().reset_index()
    
    fig = px.pie(
        archetype_counts,
        values='total_matches',
        names='archetype_type',
        title=t('archetype_distribution', lang),
        hole=0.4,
        color_discrete_sequence=px.colors.qualitative.Pastel
    )
    
    fig.update_traces(textposition='inside', textinfo='percent+label')
    fig.update_layout(height=400)
    
    st.plotly_chart(fig, use_container_width=True)


def display_deck_matchups(deck_id: int, deck_name: str, all_matchups: List[Dict], lang: str = 'en'):
    """Display win rates for a specific deck against all other decks."""
    if not all_matchups:
        st.warning(t('no_matchup_data', lang))
        return
    
    st.subheader(f"⚔️ {deck_name} - {t('matchup_analysis', lang)}")
    
    # Filter matchups for the selected deck
    deck_matchups = []
    for matchup in all_matchups:
        if matchup['deck_a_id'] == deck_id:
            deck_matchups.append({
                'opponent': matchup['deck_b_name'],
                'opponent_id': matchup['deck_b_id'],
                'matches': matchup['total_matches'],
                'wins': matchup['deck_a_wins'],
                'losses': matchup['deck_a_losses'],
                'draws': matchup['draws'],
                'win_rate': matchup['deck_a_win_rate_percentage']
            })
        elif matchup['deck_b_id'] == deck_id:
            deck_matchups.append({
                'opponent': matchup['deck_a_name'],
                'opponent_id': matchup['deck_a_id'],
                'matches': matchup['total_matches'],
                'wins': matchup['deck_a_losses'],  # B's wins = A's losses
                'losses': matchup['deck_a_wins'],   # B's losses = A's wins
                'draws': matchup['draws'],
                'win_rate': matchup['deck_b_win_rate_percentage']
            })
    
    if not deck_matchups:
        st.info(t('no_matchup_for_deck', lang).format(deck_name=deck_name))
        return
    
    # Convert to DataFrame
    df = pd.DataFrame(deck_matchups)
    df = df.sort_values('win_rate', ascending=False)
    
    # Create win rate chart
    fig = px.bar(
        df,
        x='opponent',
        y='win_rate',
        title=t('deck_matchup_title', lang).format(deck_name=deck_name),
        labels={'opponent': t('opponent_deck', lang), 'win_rate': t('win_rate_pct', lang)},
        text='win_rate',
        color='win_rate',
        color_continuous_scale=['#d62728', '#ff7f0e', '#2ca02c'],  # Red to Green
        range_color=[0, 100]
    )
    
    fig.update_traces(texttemplate='%{text:.1f}%', textposition='outside')
    fig.update_layout(
        xaxis_tickangle=-45,
        height=500,
        showlegend=False
    )
    
    st.plotly_chart(fig, use_container_width=True)
    
    # Summary metrics
    col1, col2, col3, col4 = st.columns(4)
    
    total_matches = df['matches'].sum()
    total_wins = df['wins'].sum()
    total_losses = df['losses'].sum()
    overall_wr = (total_wins / (total_wins + total_losses) * 100) if (total_wins + total_losses) > 0 else 0
    
    with col1:
        st.metric(t('total_matchups', lang), int(total_matches))
    with col2:
        st.metric(t('overall_win_rate', lang), f"{overall_wr:.1f}%")
    with col3:
        best_matchup = df.iloc[0] if len(df) > 0 else None
        if best_matchup is not None:
            st.metric(t('best_matchup', lang), best_matchup['opponent'], f"{best_matchup['win_rate']:.1f}%")
    with col4:
        worst_matchup = df.iloc[-1] if len(df) > 0 else None
        if worst_matchup is not None:
            st.metric(t('worst_matchup', lang), worst_matchup['opponent'], f"{worst_matchup['win_rate']:.1f}%")
    
    # Detailed matchup table
    with st.expander(f"📋 {t('detailed_matchup_data', lang)}"):
        display_df = df[['opponent', 'matches', 'wins', 'draws', 'losses', 'win_rate']].copy()
        display_df.columns = [t('opponent', lang), t('matches', lang), t('wins', lang), 
                             t('draws', lang), t('losses', lang), t('win_rate_pct', lang)]
        
        # Color code win rates
        def color_win_rate(val):
            if pd.isna(val):
                return ''
            if val >= 60:
                return 'background-color: #d4edda'  # Green
            elif val >= 45:
                return 'background-color: #fff3cd'  # Yellow
            else:
                return 'background-color: #f8d7da'  # Red
        
        styled_df = display_df.style.applymap(color_win_rate, subset=['Win Rate %'])
        st.dataframe(styled_df, use_container_width=True, hide_index=True)


def display_tournament_results(matches: List[Dict], tournament_name: str, lang: str = 'en'):
    """Display tournament match results."""
    if not matches:
        st.warning(t('no_matches_yet', lang))
        return
    
    st.subheader(f"🏆 {tournament_name} - {t('match_results', lang)}")
    
    # Convert to DataFrame
    df = pd.DataFrame(matches)
    
    # Create match summary
    st.markdown(f"**{t('total_matches', lang)}:** {len(df)}")
    
    # Display by rounds
    if 'round_number' in df.columns:
        rounds = sorted(df['round_number'].unique())
        
        for round_num in rounds:
            with st.expander(f"🎯 {t('round', lang)} {round_num}", expanded=(round_num == 1)):
                round_matches = df[df['round_number'] == round_num]
                
                for idx, match in round_matches.iterrows():
                    col1, col2, col3 = st.columns([2, 1, 2])
                    
                    # Get player and deck names with fallbacks
                    p1_name = match.get('player1_name', f"Player {match.get('player1_id')}")
                    p1_deck = match.get('player1_deck_name', f"Deck {match.get('player1_deck_id')}")
                    p2_name = match.get('player2_name', f"Player {match.get('player2_id')}")
                    p2_deck = match.get('player2_deck_name', f"Deck {match.get('player2_deck_id')}")
                    
                    with col1:
                        st.markdown(f"**{t('player_1', lang)}:** {p1_name}\n\n*Deck: {p1_deck}*")
                    
                    with col2:
                        st.markdown(f"<div style='text-align: center; font-weight: bold; color: #1f77b4;'>VS</div>", 
                                  unsafe_allow_html=True)
                    
                    with col3:
                        st.markdown(f"**{t('player_2', lang)}:** {p2_name}\n\n*Deck: {p2_deck}*")
                    
                    # Display games if available
                    if 'games' in match and match['games']:
                        games_data = []
                        for game in match['games']:
                            winner = game.get('winner_id')
                            game_num = game.get('game_number')
                            duration = game.get('duration_minutes', 'N/A')
                            games_data.append({
                                t('game', lang): game_num,
                                t('winner', lang): f"Player {winner}",
                                t('duration_min', lang): duration
                            })
                        
                        if games_data:
                            games_df = pd.DataFrame(games_data)
                            st.dataframe(games_df, use_container_width=True, hide_index=True)
                    
                    st.markdown(f"**{t('status', lang)}:** {match.get('match_status', 'Unknown')}")
                    
                    if 'match_date' in match:
                        st.markdown(f"*{t('date', lang)}: {match['match_date']}*")
                    
                    st.markdown("---")
    
    # Summary statistics
    col1, col2, col3 = st.columns(3)
    
    with col1:
        completed = len(df[df['match_status'] == 'COMPLETED']) if 'match_status' in df.columns else 0
        st.metric(f"✅ {t('completed_matches', lang)}", completed)
    
    with col2:
        in_progress = len(df[df['match_status'] == 'IN_PROGRESS']) if 'match_status' in df.columns else 0
        st.metric(f"⏳ {t('in_progress', lang)}", in_progress)
    
    with col3:
        total_rounds = df['round_number'].max() if 'round_number' in df.columns else 0
        st.metric(f"🎯 {t('total_rounds', lang)}", int(total_rounds))
    
    # Detailed match table
    with st.expander("📋 View All Matches Table"):
        display_cols = ['round_number', 'player1_id', 'player2_id', 'player1_deck_id', 'player2_deck_id', 'match_status']
        available_cols = [col for col in display_cols if col in df.columns]
        
        if available_cols:
            display_df = df[available_cols].copy()
            display_df.columns = [col.replace('_', ' ').title() for col in available_cols]
            st.dataframe(display_df, use_container_width=True, hide_index=True)


def main():
    """Main application function."""
    
    # Get current language
    lang = st.session_state.language
    
    # Header
    st.markdown(f'<div class="main-header">🎴 {t("app_title", lang)}</div>', unsafe_allow_html=True)
    
    # Sidebar - Language selector at top
    language_options = {
        '🇺🇸 English': 'en',
        '🇪🇸 Español': 'es'
    }
    
    selected_language = st.sidebar.selectbox(
        t('language', lang),
        options=list(language_options.keys()),
        index=0 if lang == 'en' else 1,
        key='language_selector'
    )
    
    # Update language if changed
    new_lang = language_options[selected_language]
    if new_lang != st.session_state.language:
        st.session_state.language = new_lang
        st.rerun()
    
    st.sidebar.title("⚙️ Settings")
    
    # Fetch seasons
    seasons = get_seasons()
    
    if not seasons:
        st.error(f"{t('api_unavailable', lang)} {API_BASE_URL}")
        st.info("Start the API with: `uvicorn app.main:app --reload`")
        return
    
    # Season selector
    season_options = {f"{s['name']} ({s['id']})": s['id'] for s in seasons}
    selected_season_name = st.sidebar.selectbox(
        t('select_season', lang),
        options=list(season_options.keys()),
        index=0
    )
    selected_season_id = season_options[selected_season_name]
    
    # Get selected season details
    selected_season = next((s for s in seasons if s['id'] == selected_season_id), None)
    
    # Display season info in sidebar
    if selected_season:
        st.sidebar.markdown(f"### {t('season_info', lang)}")
        st.sidebar.markdown(f"**{t('start_date', lang)}:** {selected_season['start_date']}")
        if selected_season.get('end_date'):
            st.sidebar.markdown(f"**{t('end_date', lang)}:** {selected_season['end_date']}")
        if selected_season.get('description'):
            st.sidebar.markdown(f"**{t('description', lang)}:** {selected_season['description']}")
    
    # Refresh button
    if st.sidebar.button(f"🔄 {t('refresh_data', lang)}"):
        st.cache_data.clear()
        st.rerun()
    
    # Main content tabs
    tab1, tab2, tab3, tab4 = st.tabs([
        t('tab_standings', lang), 
        t('tab_deck_stats', lang), 
        t('tab_tournament_results', lang), 
        t('tab_import', lang)
    ])
    
    with tab1:
        standings = get_season_standings(selected_season_id)
        if standings:
            display_season_standings(standings, selected_season['name'])
        else:
            st.info(t('no_standings', lang))
    
    with tab2:
        deck_stats = get_deck_statistics()
        if deck_stats:
            # Add deck filter selector
            st.subheader("🎴 Deck Performance Analysis")
            
            col_filter, col_spacer = st.columns([1, 3])
            with col_filter:
                deck_filter_options = {"All Decks": None}
                deck_filter_options.update({d['deck_name']: d['deck_id'] for d in deck_stats})
                
                selected_deck_name = st.selectbox(
                    "Filter by Deck",
                    options=list(deck_filter_options.keys()),
                    key="deck_filter"
                )
                selected_deck_id = deck_filter_options[selected_deck_name]
            
            # Show overall stats or specific deck matchups
            if selected_deck_id is None:
                # Show overall deck statistics
                col1, col2 = st.columns([2, 1])
                with col1:
                    display_deck_statistics(deck_stats, lang)
                with col2:
                    display_archetype_distribution(deck_stats, lang)
            else:
                # Show specific deck matchup analysis
                all_matchups = get_deck_matchups()
                selected_deck = next((d for d in deck_stats if d['deck_id'] == selected_deck_id), None)
                
                if selected_deck:
                    # Show deck info
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.info(f"**{t('type', lang)}:** {selected_deck.get('archetype_type', 'N/A')}")
                    with col2:
                        st.info(f"**{t('colors', lang)}:** {selected_deck.get('color_identity', 'N/A')}")
                    with col3:
                        st.info(f"**{t('win_rate', lang)}:** {selected_deck.get('win_rate_percentage', 0):.1f}%")
                    with col4:
                        st.info(f"**{t('matches', lang)}:** {selected_deck.get('total_matches', 0)}")
                    
                    st.markdown("---")
                    
                    # Display matchup analysis
                    display_deck_matchups(selected_deck_id, selected_deck['deck_name'], all_matchups, lang)
        else:
            st.info(t('no_deck_stats', lang))
    
    with tab3:
        st.subheader(f"🏆 {t('tournament_results_title', lang)}")
        
        # Fetch tournaments for selected season
        tournaments = get_tournaments(selected_season_id)
        
        if not tournaments:
            st.info(t('no_tournaments_found', lang))
        else:
            # Tournament selector
            tournament_options = {f"{t['name']} - {t['tournament_date']}": t['id'] for t in tournaments}
            selected_tournament_name = st.selectbox(
                t('select_tournament', lang),
                options=list(tournament_options.keys()),
                key="tournament_selector"
            )
            
            if selected_tournament_name:
                selected_tournament_id = tournament_options[selected_tournament_name]
                selected_tournament = next((t for t in tournaments if t['id'] == selected_tournament_id), None)
                
                # Display tournament info
                if selected_tournament:
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.info(f"**{t('location', lang)}:** {selected_tournament.get('location', 'N/A')}")
                    with col2:
                        st.info(f"**{t('format', lang)}:** {selected_tournament.get('format', 'N/A')}")
                    with col3:
                        type_name = (
                            selected_tournament.get('tournament_type', {}).get('name')
                            or selected_tournament.get('tournament_type_name')
                            or 'LGS Tournament'
                        )
                        st.info(f"**{t('type', lang)}:** {type_name}")
                    with col4:
                        st.info(f"**{t('date', lang)}:** {selected_tournament.get('tournament_date', 'N/A')}")
                
                # Fetch and display matches
                matches = get_tournament_matches(selected_tournament_id)
                display_tournament_results(matches, selected_tournament_name, lang)
    
    with tab4:
        st.subheader(t('import_title', lang))
        
        st.markdown(t('import_intro', lang))
        
        # Instructions expander
        with st.expander(t('json_format', lang)):
            st.markdown(t('json_instructions', lang))
            
            st.code("""
{
  "season_id": 1,
  "tournament": {
    "name": "Friday Night Magic",
        "tournament_date": "2026-01-10",
    "location": "Local Game Store",
        "format": "Standard",
        "tournament_type_name": "LGS Tournament"
  },
  "players": [
    {"name": "Player 1", "email": "player1@email.com"}
  ],
  "decks": [
    {"name": "Deck Name", "color_identity": "WU", "archetype_type": "Control"}
  ],
  "matches": [
    {
      "round_number": 1,
      "player1_name": "Player 1",
      "player2_name": "Player 2",
      "player1_deck_name": "Deck Name",
      "player2_deck_name": "Deck Name 2",
      "games": [
        {"game_number": 1, "winner_name": "Player 1", "duration_minutes": 20}
      ]
    }
  ]
}
            """, language="json")
        
        # File uploader
        uploaded_file = st.file_uploader(
            t('choose_file', lang),
            type=['json'],
            help=t('upload_file', lang)
        )
        
        if uploaded_file is not None:
            try:
                # Read and parse JSON
                import json
                file_contents = uploaded_file.read()
                tournament_data = json.loads(file_contents)

                # Default tournament type to LGS Tournament when not provided
                if isinstance(tournament_data, dict):
                    tournament_section = tournament_data.get("tournament", {}) or {}
                    if (
                        isinstance(tournament_section, dict)
                        and not tournament_section.get("tournament_type_id")
                        and not tournament_section.get("tournament_type_name")
                    ):
                        tournament_section["tournament_type_name"] = "LGS Tournament"
                        tournament_data["tournament"] = tournament_section
                
                # Display preview
                st.success(t('import_success', lang))
                
                with st.expander(t('preview_data', lang)):
                    st.json(tournament_data)
                    
                    # Show summary
                    st.markdown(f"### {t('import_results', lang)}")
                    col1, col2, col3, col4 = st.columns(4)
                    with col1:
                        st.metric(t('num_players', lang), len(tournament_data.get('players', [])))
                    with col2:
                        st.metric(t('num_decks', lang), len(tournament_data.get('decks', [])))
                    with col3:
                        st.metric(t('num_matches', lang), len(tournament_data.get('matches', [])))
                    with col4:
                        total_games = sum(len(m.get('games', [])) for m in tournament_data.get('matches', []))
                        st.metric(t('created_games', lang), total_games)
                
                # Import button
                if st.button(f"🚀 {t('import_button', lang)}", type="primary", use_container_width=True):
                    with st.spinner(t('import_in_progress', lang) if lang == 'es' else "Importing tournament data..."):
                        try:
                            response = requests.post(
                                f"{API_BASE_URL}/tournaments/import-complete",
                                json=tournament_data,
                                timeout=30
                            )
                            
                            if response.status_code in [200, 201]:
                                result = response.json()
                                st.success(t('import_success', lang))
                                
                                # Display results
                                st.markdown(f"### {t('import_results', lang)}")
                                col1, col2, col3, col4, col5 = st.columns(5)
                                with col1:
                                    st.metric("Tournament", "✓" if result['tournament_created'] else "Exists")
                                with col2:
                                    st.metric(t('created_players', lang), result['players_created'])
                                with col3:
                                    st.metric(t('created_decks', lang), result['decks_created'])
                                with col4:
                                    st.metric(t('created_matches', lang), result['matches_created'])
                                with col5:
                                    st.metric(t('created_games', lang), result['games_created'])
                                
                                st.info(result['message'])
                                
                                # Clear cache to show new data
                                st.cache_data.clear()
                                
                            else:
                                error_detail = response.json().get('detail', 'Unknown error')
                                st.error(f"{t('import_error', lang)}: {error_detail}")
                                
                        except requests.exceptions.RequestException as e:
                            st.error(f"{t('import_error', lang)}: {str(e)}")
                        except Exception as e:
                            st.error(f"{t('import_error', lang)}: {str(e)}")
                            
            except json.JSONDecodeError as e:
                st.error(f"{t('invalid_json', lang)}: {str(e)}")
            except Exception as e:
                st.error(f"{t('import_error', lang)}: {str(e)}")
        else:
            st.info(t('upload_file_first', lang))
    
    # Footer
    st.markdown("---")
    st.markdown(
        "Built with ❤️ using Streamlit | Data from MTG Tournament Tracker API",
        unsafe_allow_html=True
    )


if __name__ == "__main__":
    main()
