"""
Translation dictionary for MTG Tournament Tracker UI
Supports English and Spanish localization for UI components only.
Game-specific terms (match, deck, winrate, etc.) remain in English.
"""

TRANSLATIONS = {
    'en': {
        # Common/General
        'app_title': 'MTG Tournament Tracker',
        'app_subtitle': 'Displays season standings, deck statistics, and tournament results with interactive visualizations.',
        'language': 'Language',
        
        # Sidebar
        'select_season': 'Select Season',
        'season_info': 'Season Information',
        'start_date': 'Start Date',
        'end_date': 'End Date',
        'description': 'Description',
        'refresh_data': 'Refresh Data',
        
        # Tabs
        'tab_standings': '📊 Season Standings',
        'tab_deck_stats': '🎴 Deck Statistics',
        'tab_tournament_results': '🏆 Tournament Results',
        'tab_import': '📤 Import Tournament',
        
        # Season Standings
        'standings_title': '📊 {season} - Standings',
        'position': 'Position',
        'pos': 'Pos',
        'player': 'Player',
        'matches_played': 'MP',
        'wins': 'W',
        'draws': 'D',
        'losses': 'L',
        'points': 'Points',
        'champion': '🏆 Champion',
        'record': 'Record (W-D-L)',
        'no_standings': 'No standings data available for this season.',
        'how_calculated': 'ℹ️ How are standings calculated?',
        'calculation_explanation': '''**Points are awarded based on tournament type:**

| Tournament Type | Points/Win | Points/Draw |
|----------------|-----------|-------------|
| Nationals | 12 | 4 |
| Special Event | 7 | 3 |
| LGS Tournament | 5 | 2 |
| Online Tournament | 3 | 0 |

- **Match Win**: Player earns points based on the tournament type
- **Match Draw**: Both players earn draw points (if applicable)
- **Match Loss**: No points awarded

Your season total is the sum of all points earned across all tournaments. 
For more details, see the [Standings Calculation Guide](STANDINGS_CALCULATION.md).
''',
        
        # Deck Statistics
        'deck_stats_title': '🎴 Deck Performance Analysis',
        'filter_by_deck': 'Filter by Deck',
        'all_decks': 'All Decks',
        'win_rates': 'Deck Win Rates',
        'deck_name': 'Deck Name',
        'win_rate_pct': 'Win Rate %',
        'archetype': 'Archetype',
        'meta_analysis': '📈 Meta Analysis',
        'top_performing': 'Top Performing',
        'meta_share': 'Meta Share',
        'total_matches': 'Total Matches',
        'deck_details': 'Deck Details',
        'detailed_stats': 'Detailed Statistics',
        'archetype_distribution': '🎯 Archetype Distribution',
        'matchup_analysis': '⚔️ Matchup Analysis',
        'best_matchups': 'Best Matchups',
        'worst_matchups': 'Worst Matchups',
        'no_deck_stats': 'No deck statistics available.',
        'no_matchups': 'No matchup data available for this deck.',
        'no_matchup_data': 'No matchup data available.',
        'no_matchup_for_deck': 'No matchup data available for {deck_name} yet.',
        'select_deck_first': '👆 Select a specific deck to see matchup analysis',
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
        'tournament_results_title': '🏆 Tournament Results',
        'select_tournament': 'Select Tournament',
        'location': '**Location:**',
        'format': '**Format:**',
        'type': '**Type:**',
        'date': '**Date:**',
        'round': '🎯 Round {round_num}',
        'player_1': '**Player 1:**',
        'player_2': '**Player 2:**',
        'deck_label': '*Deck: {deck}*',
        'status': '**Status:**',
        'game': 'Game',
        'winner': 'Winner',
        'duration': 'Duration (min)',
        'completed_matches': '✅ Completed Matches',
        'in_progress': '⏳ In Progress',
        'total_rounds': '🎯 Total Rounds',
        'no_tournaments': 'No tournaments found for this season.',
        'no_matches': 'No matches recorded for this tournament yet.',
        
        # Import Tournament
        'import_title': '📤 Import Tournament Data',
        'import_intro': '''Upload a JSON file containing complete tournament data including players, decks, matches, and games.
The system will automatically create any missing players or decks.''',
        'json_format': '📋 JSON Format Instructions',
        'json_instructions': '''Your JSON file should include:
- **season_id**: The ID of the season for this tournament
- **tournament**: Name, date, location, format, and optional tournament type (defaults to "LGS Tournament" if omitted)
- **players**: List of players (name and optional email)
- **decks**: List of deck archetypes (name, colors, archetype)
- **matches**: List of matches with round, players, decks, and games

Download the template or example files from the UI folder to get started.''',
        'upload_file': 'Upload JSON File',
        'choose_file': 'Choose a JSON file',
        'preview_data': '👀 Preview Data',
        'season_id': 'Season ID',
        'tournament_name': 'Tournament Name',
        'tournament_date': 'Tournament Date',
        'num_players': 'Number of Players',
        'num_decks': 'Number of Decks',
        'num_matches': 'Number of Matches',
        'import_button': 'Import Tournament',
        'import_in_progress': 'Importing tournament data...',
        'import_success': '✅ Tournament imported successfully!',
        'import_results': 'Import Results',
        'created_players': 'Players Created',
        'created_decks': 'Decks Created',
        'created_matches': 'Matches Created',
        'created_games': 'Games Created',
        'import_error': '❌ Import failed',
        'invalid_json': '❌ Invalid JSON file. Please check the format.',
        'upload_file_first': 'Please upload a file first.',
        
        # Error Messages
        'error_seasons': 'Error fetching seasons',
        'error_standings': 'Error fetching season standings',
        'error_tournaments': 'Error fetching tournaments',
        'error_matches': 'Error fetching matches',
        'error_decks': 'Error fetching deck statistics',
        'error_matchups': 'Error fetching matchup data',
        'error_import': 'Error importing tournament',
        'api_unavailable': 'Unable to connect to API. Please ensure the backend is running.',
    },
    'es': {
        # Common/General
        'app_title': 'Rastreador de Torneos MTG',
        'app_subtitle': 'Muestra clasificaciones de temporada, estadísticas de decks y resultados de torneos con visualizaciones interactivas.',
        'language': 'Idioma',
        
        # Sidebar
        'select_season': 'Seleccionar Temporada',
        'season_info': 'Información de Temporada',
        'start_date': 'Fecha de Inicio',
        'end_date': 'Fecha de Fin',
        'description': 'Descripción',
        'refresh_data': 'Actualizar Datos',
        
        # Tabs
        'tab_standings': '📊 Clasificación',
        'tab_deck_stats': '🎴 Estadísticas de Decks',
        'tab_tournament_results': '🏆 Resultados de Torneos',
        'tab_import': '📤 Importar Torneo',
        
        # Season Standings
        'standings_title': '📊 {season} - Clasificación',
        'position': 'Posición',
        'pos': 'Pos',
        'player': 'Jugador',
        'matches_played': 'PJ',
        'wins': 'G',
        'draws': 'E',
        'losses': 'P',
        'points': 'Puntos',
        'champion': '🏆 Campeón',
        'record': 'Récord (G-E-P)',
        'no_standings': 'No hay datos de clasificación disponibles para esta temporada.',
        'how_calculated': 'ℹ️ ¿Cómo se calculan las clasificaciones?',
        'calculation_explanation': '''**Los puntos se otorgan según el tipo de torneo:**

| Tipo de Torneo | Puntos/Victoria | Puntos/Empate |
|----------------|----------------|---------------|
| Nationals | 12 | 4 |
| Special Event | 7 | 3 |
| LGS Tournament | 5 | 2 |
| Online Tournament | 3 | 0 |

- **Victoria en Match**: El jugador gana puntos según el tipo de torneo
- **Empate en Match**: Ambos jugadores ganan puntos de empate (si aplica)
- **Derrota en Match**: No se otorgan puntos

Tu total de temporada es la suma de todos los puntos ganados en todos los torneos. 
Para más detalles, consulta la [Guía de Cálculo de Clasificaciones](STANDINGS_CALCULATION.md).
''',
        
        # Deck Statistics
        'deck_stats_title': '🎴 Análisis de Rendimiento de Decks',
        'filter_by_deck': 'Filtrar por Deck',
        'all_decks': 'Todos los Decks',
        'win_rates': 'Tasas de Victoria de Decks',
        'deck_name': 'Nombre del Deck',
        'win_rate_pct': 'Tasa de Victoria %',
        'archetype': 'Arquetipo',
        'meta_analysis': '📈 Análisis del Meta',
        'top_performing': 'Mejor Rendimiento',
        'meta_share': 'Cuota del Meta',
        'total_matches': 'Total de Partidas',
        'deck_details': 'Detalles del Deck',
        'detailed_stats': 'Estadísticas Detalladas',
        'archetype_distribution': '🎯 Distribución de Arquetipos',
        'matchup_analysis': '⚔️ Análisis de Enfrentamientos',
        'best_matchups': 'Mejores Enfrentamientos',
        'worst_matchups': 'Peores Enfrentamientos',
        'no_deck_stats': 'No hay estadísticas de decks disponibles.',
        'no_matchups': 'No hay datos de enfrentamientos disponibles para este deck.',
        'no_matchup_data': 'No hay datos de enfrentamientos disponibles.',
        'no_matchup_for_deck': 'Aún no hay datos de enfrentamientos disponibles para {deck_name}.',
        'select_deck_first': '👆 Selecciona un deck específico para ver el análisis de enfrentamientos',
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
        'tournament_results_title': '🏆 Resultados de Torneos',
        'select_tournament': 'Seleccionar Torneo',
        'location': '**Ubicación:**',
        'format': '**Formato:**',
        'type': '**Tipo:**',
        'date': '**Fecha:**',
        'round': '🎯 Ronda {round_num}',
        'player_1': '**Jugador 1:**',
        'player_2': '**Jugador 2:**',
        'deck_label': '*Deck: {deck}*',
        'status': '**Estado:**',
        'game': 'Juego',
        'winner': 'Ganador',
        'duration': 'Duración (min)',
        'completed_matches': '✅ Partidas Completadas',
        'in_progress': '⏳ En Progreso',
        'total_rounds': '🎯 Total de Rondas',
        'no_tournaments': 'No se encontraron torneos para esta temporada.',
        'no_matches': 'Aún no se han registrado partidas para este torneo.',
        
        # Import Tournament
        'import_title': '📤 Importar Datos de Torneo',
        'import_intro': '''Sube un archivo JSON con datos completos del torneo incluyendo jugadores, decks, partidas y juegos.
El sistema creará automáticamente cualquier jugador o deck faltante.''',
        'json_format': '📋 Instrucciones del Formato JSON',
        'json_instructions': '''Tu archivo JSON debe incluir:
- **season_id**: El ID de la temporada para este torneo
- **tournament**: Nombre, fecha, ubicación, formato y tipo de torneo opcional (por defecto "LGS Tournament" si se omite)
- **players**: Lista de jugadores (nombre y email opcional)
- **decks**: Lista de arquetipos de decks (nombre, colores, arquetipo)
- **matches**: Lista de partidas con ronda, jugadores, decks y juegos

Descarga la plantilla o archivos de ejemplo de la carpeta UI para comenzar.''',
        'upload_file': 'Subir Archivo JSON',
        'choose_file': 'Elige un archivo JSON',
        'preview_data': '👀 Vista Previa de Datos',
        'season_id': 'ID de Temporada',
        'tournament_name': 'Nombre del Torneo',
        'tournament_date': 'Fecha del Torneo',
        'num_players': 'Número de Jugadores',
        'num_decks': 'Número de Decks',
        'num_matches': 'Número de Partidas',
        'import_button': 'Importar Torneo',
        'import_in_progress': 'Importando datos del torneo...',
        'import_success': '✅ ¡Torneo importado exitosamente!',
        'import_results': 'Resultados de Importación',
        'created_players': 'Jugadores Creados',
        'created_decks': 'Decks Creados',
        'created_matches': 'Partidas Creadas',
        'created_games': 'Juegos Creados',
        'import_error': '❌ Falló la importación',
        'invalid_json': '❌ Archivo JSON inválido. Por favor verifica el formato.',
        'upload_file_first': 'Por favor sube un archivo primero.',
        
        # Error Messages
        'error_seasons': 'Error al obtener temporadas',
        'error_standings': 'Error al obtener clasificaciones',
        'error_tournaments': 'Error al obtener torneos',
        'error_matches': 'Error al obtener partidas',
        'error_decks': 'Error al obtener estadísticas de decks',
        'error_matchups': 'Error al obtener datos de enfrentamientos',
        'error_import': 'Error al importar torneo',
        'api_unavailable': 'No se puede conectar a la API. Por favor asegúrate de que el backend esté funcionando.',
    }
}


def t(key: str, lang: str = 'en', **kwargs) -> str:
    """
    Get translated text for the given key.
    
    Args:
        key: Translation key (e.g., 'app_title', 'select_season')
        lang: Language code ('en' or 'es')
        **kwargs: Optional format arguments for string interpolation
    
    Returns:
        Translated string, or the key itself if translation not found
    """
    try:
        text = TRANSLATIONS.get(lang, TRANSLATIONS['en']).get(key, key)
        if kwargs:
            return text.format(**kwargs)
        return text
    except (KeyError, AttributeError):
        return key
