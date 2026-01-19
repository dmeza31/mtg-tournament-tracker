"""
Translation dictionary and helper for MTG Tournament Tracker UI.
Supports English and Spanish localization for UI components. Game-specific
terms (match, deck, winrate, etc.) stay in English for clarity.
"""

TRANSLATIONS = {
    'en': {
        # Common/General
        'app_title': 'MTG Tournament Tracker',
        'app_subtitle': 'Displays season standings, deck statistics, and tournament results with interactive visualizations.',
        'language': 'Language',

        # Tabs
        'tab_standings': 'Standings',
        'tab_deck_stats': 'Deck Statistics',
        'tab_tournament_results': 'Tournament Results',

        # Sidebar
        'select_season': 'Select Season',
        'season_info': 'Season Information',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'description': 'Description',
        'refresh_data': 'Refresh Data',

        # Standings
        'standings_title': '{season} Standings',
        'no_standings': 'No standings available for this season yet.',
        'pos': 'Pos',
        'player': 'Player',
        'matches_played': 'Matches Played',
        'wins': 'Wins',
        'draws': 'Draws',
        'losses': 'Losses',
        'points': 'Points',
        'champion': 'Champion',
        'record': 'Record',
        'how_calculated': 'How standings are calculated',
        'calculation_explanation': (
            "Standings points use tournament type multipliers:\n\n"
            "| Tournament Type | Points/Win | Points/Draw |\n"
            "|-----------------|------------|-------------|\n"
            "| Nationals       | 12         | 4           |\n"
            "| Special Event   | 7          | 3           |\n"
            "| LGS Tournament  | 5          | 2           |\n"
            "| Online Tournament| 3         | 0           |"
        ),

        # Deck Statistics
        'deck_stats_title': 'Deck Performance Analysis',
        'filter_by_deck': 'Filter by Deck',
        'all_decks': 'All Decks',
        'win_rates': 'Deck Win Rates',
        'deck_name': 'Deck Name',
        'win_rate_pct': 'Win Rate %',
        'archetype': 'Archetype',
        'meta_analysis': 'Meta Analysis',
        'top_performing': 'Top Performing',
        'meta_share': 'Meta Share',
        'total_matches': 'Total Matches',
        'deck_details': 'Deck Details',
        'detailed_stats': 'Detailed Statistics',
        'archetype_distribution': 'Archetype Distribution',
        'matchup_analysis': 'Matchup Analysis',
        'best_matchups': 'Best Matchups',
        'worst_matchups': 'Worst Matchups',
        'no_deck_stats': 'No deck statistics available.',
        'no_matchups': 'No matchup data available for this deck.',
        'no_matchup_data': 'No matchup data available.',
        'no_matchup_for_deck': 'No matchup data available for {deck_name} yet.',
        'select_deck_first': 'Select a specific deck to see matchup analysis',
        'vs': 'vs',
        'deck': 'Deck',
        'type': 'Type',
        'colors': 'Colors',
        'matches': 'Matches',
        'players': 'Players',
        'tournaments': 'Tournaments',
        'win_rate': 'Win Rate',
        'opponent': 'Opponent',
        'opponent_deck': 'Opponent Deck',
        'deck_matchup_title': '{deck_name} Win Rate by Matchup',
        'total_matchups': 'Total Matchups Played',
        'overall_win_rate': 'Overall Win Rate',
        'best_matchup': 'Best Matchup',
        'worst_matchup': 'Worst Matchup',
        'detailed_matchup_data': 'View Detailed Matchup Data',
        'match_results': 'Match Results',
        'no_matches_yet': 'No matches recorded for this tournament yet.',
        'no_tournaments_found': 'No tournaments found for this season.',
        'round': 'Round',
        'duration_min': 'Duration (min)',

        # Tournament Results
        'tournament_results_title': 'Tournament Results',
        'select_tournament': 'Select Tournament',
        'location': 'Location',
        'format': 'Format',
        'type': 'Type',
        'date': 'Date',
        'player_1': 'Player 1',
        'player_2': 'Player 2',
        'deck_label': 'Deck: {deck}',
        'status': 'Status',
        'match_winner': 'Match Winner',
        'game': 'Game',
        'winner': 'Winner',
        'duration': 'Duration (min)',
        'completed_matches': 'Completed Matches',
        'in_progress': 'In Progress',
        'total_rounds': 'Total Rounds',
        'no_tournaments': 'No tournaments found for this season.',
        'no_matches': 'No matches recorded for this tournament yet.',

        # Error Messages
        'error_seasons': 'Error fetching seasons',
        'error_standings': 'Error fetching season standings',
        'error_tournaments': 'Error fetching tournaments',
        'error_matches': 'Error fetching matches',
        'error_decks': 'Error fetching deck statistics',
        'error_matchups': 'Error fetching matchup data',
        'error_import': 'Error importing tournament',
        'api_unavailable': 'Unable to reach the API. Ensure the backend is running.',
    },
    'es': {
        # Common/General
        'app_title': 'MTG Tournament Tracker',
        'app_subtitle': 'Muestra clasificaciones de temporada, estadísticas de decks y resultados de torneos con visualizaciones interactivas.',
        'language': 'Idioma',

        # Tabs
        'tab_standings': 'Clasificaciones',
        'tab_deck_stats': 'Estadísticas de Decks',
        'tab_tournament_results': 'Resultados de Torneos',

        # Sidebar
        'select_season': 'Seleccionar Temporada',
        'season_info': 'Información de la Temporada',
        'start_date': 'Fecha de Inicio',
        'end_date': 'Fecha de Fin',
        'description': 'Descripción',
        'refresh_data': 'Actualizar Datos',

        # Standings
        'standings_title': 'Clasificaciones de {season}',
        'no_standings': 'Aún no hay clasificaciones para esta temporada.',
        'pos': 'Pos',
        'player': 'Jugador',
        'matches_played': 'Partidas Jugadas',
        'wins': 'Victorias',
        'draws': 'Empates',
        'losses': 'Derrotas',
        'points': 'Puntos',
        'champion': 'Campeón',
        'record': 'Récord',
        'how_calculated': 'Cómo se calculan las clasificaciones',
        'calculation_explanation': (
            "Los puntos de clasificación usan multiplicadores según el tipo de torneo:\n\n"
            "| Tipo de Torneo  | Puntos/Victoria | Puntos/Empate |\n"
            "|-----------------|-----------------|---------------|\n"
            "| Nationals       | 12              | 4             |\n"
            "| Special Event   | 7               | 3             |\n"
            "| LGS Tournament  | 5               | 2             |\n"
            "| Online Tournament| 3              | 0             |"
        ),

        # Deck Statistics
        'deck_stats_title': 'Analisis de Rendimiento de Decks',
        'filter_by_deck': 'Filtrar por Deck',
        'all_decks': 'Todos los Decks',
        'win_rates': 'Tasas de Victoria de Decks',
        'deck_name': 'Nombre del Deck',
        'win_rate_pct': 'Tasa de Victoria %',
        'archetype': 'Arquetipo',
        'meta_analysis': 'Analisis del Meta',
        'top_performing': 'Mejor Rendimiento',
        'meta_share': 'Cuota del Meta',
        'total_matches': 'Total de Partidas',
        'deck_details': 'Detalles del Deck',
        'detailed_stats': 'Estadísticas Detalladas',
        'archetype_distribution': 'Distribucion de Arquetipos',
        'matchup_analysis': 'Analisis de Enfrentamientos',
        'best_matchups': 'Mejores Enfrentamientos',
        'worst_matchups': 'Peores Enfrentamientos',
        'no_deck_stats': 'No hay estadísticas de decks disponibles.',
        'no_matchups': 'No hay datos de enfrentamientos disponibles para este deck.',
        'no_matchup_data': 'No hay datos de enfrentamientos disponibles.',
        'no_matchup_for_deck': 'Aún no hay datos de enfrentamientos disponibles para {deck_name}.',
        'select_deck_first': 'Selecciona un deck especifico para ver el analisis de enfrentamientos',
        'vs': 'vs',
        'deck': 'Deck',
        'type': 'Tipo',
        'colors': 'Colores',
        'matches': 'Partidas',
        'players': 'Jugadores',
        'tournaments': 'Torneos',
        'win_rate': 'Tasa de Victoria',
        'opponent': 'Oponente',
        'opponent_deck': 'Deck Oponente',
        'deck_matchup_title': 'Tasa de Victoria de {deck_name} por Enfrentamiento',
        'total_matchups': 'Total de Enfrentamientos Jugados',
        'overall_win_rate': 'Tasa de Victoria General',
        'best_matchup': 'Mejor Enfrentamiento',
        'worst_matchup': 'Peor Enfrentamiento',
        'detailed_matchup_data': 'Ver Datos Detallados de Enfrentamientos',
        'match_results': 'Resultados de Partidas',
        'no_matches_yet': 'Aún no se han registrado partidas para este torneo.',
        'no_tournaments_found': 'No se encontraron torneos para esta temporada.',
        'round': 'Ronda',
        'duration_min': 'Duración (min)',

        # Tournament Results
        'tournament_results_title': 'Resultados de Torneos',
        'select_tournament': 'Seleccionar Torneo',
        'location': 'Ubicacion',
        'format': 'Formato',
        'type': 'Tipo',
        'date': 'Fecha',
        'player_1': 'Jugador 1',
        'player_2': 'Jugador 2',
        'deck_label': 'Deck: {deck}',
        'status': 'Estado',
        'match_winner': 'Ganador del Match',
        'game': 'Juego',
        'winner': 'Ganador',
        'duration': 'Duración (min)',
        'completed_matches': 'Partidas Completadas',
        'in_progress': 'En Progreso',
        'total_rounds': 'Total de Rondas',
        'no_tournaments': 'No se encontraron torneos para esta temporada.',
        'no_matches': 'Aún no se han registrado partidas para este torneo.',

        # Error Messages
        'error_seasons': 'Error al obtener temporadas',
        'error_standings': 'Error al obtener clasificaciones de temporada',
        'error_tournaments': 'Error al obtener torneos',
        'error_matches': 'Error al obtener partidas',
        'error_decks': 'Error al obtener estadísticas de decks',
        'error_matchups': 'Error al obtener datos de enfrentamientos',
        'error_import': 'Error al importar torneo',
        'api_unavailable': 'No se puede conectar con la API. Asegúrate de que el backend esté ejecutándose.',
    },
}


def t(key: str, lang: str = 'en', **kwargs) -> str:
    """Translate a key for the given language with graceful fallback."""
    translations = TRANSLATIONS.get(lang, TRANSLATIONS.get('en', {}))
    fallback = TRANSLATIONS.get('en', {})
    text = translations.get(key) or fallback.get(key) or key

    if kwargs:
        try:
            return text.format(**kwargs)
        except Exception:
            return text
    return text

