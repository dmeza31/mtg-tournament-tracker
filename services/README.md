# MTG Tournament Tracker API

A comprehensive RESTful API built with **Python FastAPI** for tracking Magic the Gathering tournament matches, player performance, and deck archetype statistics.

## Features

✅ **Complete CRUD Operations** for all entities (seasons, tournaments, players, decks, matches, games)  
✅ **Best-of-3 Match Tracking** with individual game results  
✅ **Statistics Endpoints** querying optimized database views  
✅ **Batch Match Insertion** with PostgreSQL transaction support  
✅ **Automatic API Documentation** via Swagger UI and ReDoc  
✅ **Error Handling** with structured JSON responses  
✅ **CORS Support** for web application integration  
✅ **Tournament Types** with per-event win/draw points (default LGS Tournament; accept type id or unique name)

## Tech Stack

- **FastAPI** - Modern Python web framework
- **SQLAlchemy** - ORM for database operations
- **PostgreSQL** - Database with optimized views
- **Pydantic** - Data validation and serialization
- **Uvicorn** - ASGI server

## Prerequisites

1. **Python 3.9+** - [Download Python](https://www.python.org/downloads/)
2. **PostgreSQL 12+** - [Download PostgreSQL](https://www.postgresql.org/download/)
3. **Database Schema** - Run SQL scripts from `../database/` folder first

## Installation

### 1. Create Virtual Environment

```bash
# Navigate to services directory
cd services

# Create virtual environment
python -m venv venv

# Activate virtual environment
# Windows:
venv\Scripts\activate
# Mac/Linux:
source venv/bin/activate
```

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Configure Environment

Copy `.env.example` to `.env` and update with your settings:

```bash
copy .env.example .env
```

Edit `.env` file:

```ini
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/mtg_tournaments
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
CORS_ORIGINS=http://localhost:3000,http://localhost:8080
DEBUG=True
```

### 4. Set Up Database

If you haven't already, run the database schema scripts:

```bash
# Navigate to database folder
cd ../database

# Run scripts in order
psql -U postgres -d mtg_tournaments -f 01_schema.sql
psql -U postgres -d mtg_tournaments -f 02_indexes.sql
psql -U postgres -d mtg_tournaments -f 03_views.sql

# Optional: Load sample data
psql -U postgres -d mtg_tournaments -f 05_sample_data.sql
```

## Running the API

### Development Mode

```bash
# From services directory
python -m app.main
```

Or use uvicorn directly:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

The API will be available at:
- **API**: http://localhost:8000
- **Swagger UI**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **OpenAPI JSON**: http://localhost:8000/openapi.json

### Production Mode

```bash
uvicorn app.main:app --host 0.0.0.0 --port 8000 --workers 4
```

## API Endpoints

### Seasons

- `GET /api/v1/seasons` - List all seasons
- `GET /api/v1/seasons/{id}` - Get season by ID
- `POST /api/v1/seasons` - Create new season
- `PUT /api/v1/seasons/{id}` - Update season
- `DELETE /api/v1/seasons/{id}` - Delete season

### Tournaments

- `GET /api/v1/tournaments` - List all tournaments
- `GET /api/v1/tournaments?season_id={id}` - Filter by season
- `GET /api/v1/tournaments/{id}` - Get tournament by ID
- `POST /api/v1/tournaments` - Create new tournament
- `PUT /api/v1/tournaments/{id}` - Update tournament
- `DELETE /api/v1/tournaments/{id}` - Delete tournament
- `POST /api/v1/tournaments/import-complete` - **Import complete tournament data** (players, decks, matches, games)

### Tournament Types

- `GET /api/v1/tournament-types` - List all tournament types
- `GET /api/v1/tournament-types/{id}` - Get tournament type by ID
- `POST /api/v1/tournament-types` - Create new tournament type
- `PUT /api/v1/tournament-types/{id}` - Update tournament type
- `DELETE /api/v1/tournament-types/{id}` - Delete tournament type

### Players

- `GET /api/v1/players` - List all players
- `GET /api/v1/players?active_only=true` - Filter active players
- `GET /api/v1/players/{id}` - Get player by ID
- `POST /api/v1/players` - Create new player
- `PUT /api/v1/players/{id}` - Update player
- `DELETE /api/v1/players/{id}` - Delete player

### Deck Archetypes

- `GET /api/v1/decks` - List all deck archetypes
- `GET /api/v1/decks?archetype_type=Aggro` - Filter by type
- `GET /api/v1/decks/{id}` - Get deck by ID
- `POST /api/v1/decks` - Create new deck archetype
- `PUT /api/v1/decks/{id}` - Update deck archetype
- `DELETE /api/v1/decks/{id}` - Delete deck archetype

### Matches & Games

- `GET /api/v1/matches` - List all matches
- `GET /api/v1/matches?tournament_id={id}` - Filter by tournament
- `GET /api/v1/matches?player_id={id}` - Filter by player
- `GET /api/v1/matches/{id}` - Get match by ID (with games)
- `POST /api/v1/matches` - Create new match
- `PUT /api/v1/matches/{id}` - Update match
- `DELETE /api/v1/matches/{id}` - Delete match
- `GET /api/v1/matches/{id}/games` - Get games for match
- `POST /api/v1/matches/{id}/games` - Add game to match
- `PUT /api/v1/matches/{match_id}/games/{game_id}` - Update game winner/result
- `DELETE /api/v1/matches/{id}/games/{game_id}` - Delete game
- Business rule: max 3 games per match; game_number must be unique per match (1-3)
- `POST /api/v1/matches/batch` - **Batch create matches with games**

### Statistics

- `GET /api/v1/stats/players` - Player statistics (wins, losses, win rates)
- `GET /api/v1/stats/players/{id}` - Specific player stats
- `GET /api/v1/stats/decks` - Deck archetype statistics
- `GET /api/v1/stats/decks/{id}` - Specific deck stats
- `GET /api/v1/stats/matchups` - All deck matchup data
- `GET /api/v1/stats/matchups/{deck_a_id}/{deck_b_id}` - Specific matchup
- `GET /api/v1/stats/season-standings` - Season standings with points (all seasons)
- `GET /api/v1/stats/season-standings?season_id={id}` - Filter standings by season
- `GET /api/v1/stats/season-standings/{season_id}` - Get standings for specific season

### Health & Info

- `GET /health` - Health check
- `GET /` - API information

## Usage Examples

### Create a Season

```bash
curl -X POST "http://localhost:8000/api/v1/seasons" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "2026 Standard Season",
    "start_date": "2026-01-01",
    "end_date": "2026-03-31",
    "description": "Q1 2026 Standard Season"
  }'
```

### Create a Tournament

```bash
curl -X POST "http://localhost:8000/api/v1/tournaments" \
  -H "Content-Type: application/json" \
  -d '{
    "season_id": 1,
    "name": "Friday Night Magic - Week 1",
    "tournament_date": "2026-01-10",
    "location": "Local Game Store",
    "format": "Standard",
    "tournament_type_name": "LGS Tournament"
  }'
```

**Notes:**
- `tournament_type_name` is optional (defaults to "LGS Tournament" if omitted)
- Can also use `tournament_type_id` instead of `tournament_type_name`
- Available types: Nationals, Special Event, LGS Tournament (default), Online Tournament

### Create a Player

```bash
curl -X POST "http://localhost:8000/api/v1/players" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Alice Johnson",
    "email": "alice@example.com",
    "active": true
  }'
```

### Create a Deck Archetype

```bash
curl -X POST "http://localhost:8000/api/v1/decks" \
  -H "Content-Type: application/json" \
  -d '{
    "name": "Mono Red Aggro",
    "color_identity": "R",
    "archetype_type": "Aggro",
    "description": "Fast red deck with burn spells"
  }'
```

### Batch Create Matches

```bash
curl -X POST "http://localhost:8000/api/v1/matches/batch" \
  -H "Content-Type: application/json" \
  -d '{
    "matches": [
      {
        "tournament_id": 1,
        "player1_id": 1,
        "player2_id": 2,
        "player1_deck_id": 1,
        "player2_deck_id": 2,
        "round_number": 1,
        "match_status": "COMPLETED",
        "games": [
          {"game_number": 1, "winner_id": 1, "game_result": "WIN", "duration_minutes": 12},
          {"game_number": 2, "winner_id": 2, "game_result": "WIN", "duration_minutes": 18},
          {"game_number": 3, "winner_id": 1, "game_result": "WIN", "duration_minutes": 15}
        ]
      }
    ]
  }'
```

### Get Player Statistics

```bash
curl "http://localhost:8000/api/v1/stats/players"
```

### Get Deck Matchup

```bash
curl "http://localhost:8000/api/v1/stats/matchups/1/2"
```

### Import Complete Tournament

Import a complete tournament with players, decks, and matches in a single operation:

```bash
curl -X POST "http://localhost:8000/api/v1/tournaments/import-complete" \
  -H "Content-Type: application/json" \
  -d '{
    "season_id": 1,
    "tournament": {
      "name": "Friday Night Magic",
      "tournament_date": "2026-01-10",
      "location": "Local Game Store",
      "format": "Standard",
      "tournament_type_name": "LGS Tournament"
    },
    "players": [
      {"name": "Alice", "email": "alice@email.com"},
      {"name": "Bob", "email": "bob@email.com"}
    ],
    "decks": [
      {"name": "Temur Energy", "color_identity": "URG", "archetype_type": "Midrange"},
      {"name": "Esper Control", "color_identity": "WUB", "archetype_type": "Control"}
    ],
    "matches": [
      {
        "round_number": 1,
        "player1_name": "Alice",
        "player2_name": "Bob",
        "player1_deck_name": "Temur Energy",
        "player2_deck_name": "Esper Control",
        "games": [
          {"game_number": 1, "winner_name": "Alice", "duration_minutes": 20},
          {"game_number": 2, "winner_name": "Bob", "duration_minutes": 25},
          {"game_number": 3, "winner_name": "Alice", "duration_minutes": 18}
        ]
      }
    ]
  }'
```

**Features:**
- Automatically creates missing players and decks
- Looks up existing entities by name
- Tournament type can be specified by `tournament_type_id` or `tournament_type_name` (defaults to "LGS Tournament" if omitted)
- Available tournament types: Nationals (12/4 pts), Special Event (7/3 pts), LGS Tournament (5/2 pts), Online Tournament (3/0 pts)
- Creates tournament, matches, and games in a single transaction
- Returns counts of created entities
- Full validation with detailed error messages

For more detailed examples, see [EXAMPLES.md](EXAMPLES.md).

## Project Structure

```
services/
├── app/
│   ├── __init__.py
│   ├── main.py              # FastAPI application
│   ├── config.py            # Configuration management
│   ├── database.py          # Database connection
│   ├── models.py            # SQLAlchemy ORM models
│   ├── schemas.py           # Pydantic schemas
│   ├── crud/                # Database operations
│   │   ├── seasons.py
│   │   ├── tournaments.py
│   │   ├── players.py
│   │   ├── decks.py
│   │   ├── matches.py
│   │   └── statistics.py
│   └── routers/             # API endpoints
│       ├── seasons.py
│       ├── tournaments.py
│       ├── players.py
│       ├── decks.py
│       ├── matches.py
│       └── statistics.py
├── .env                     # Environment variables (create from .env.example)
├── .env.example             # Environment template
├── .gitignore
├── requirements.txt
├── README.md                # This file
└── EXAMPLES.md              # Detailed API examples
```

## API Documentation

The API includes **automatic interactive documentation**:

### Swagger UI
Visit http://localhost:8000/docs for:
- Interactive API testing
- Request/response schemas
- Try out endpoints directly in browser
- Example values for all fields

### ReDoc
Visit http://localhost:8000/redoc for:
- Clean, readable documentation
- Detailed schema documentation
- Code samples

### OpenAPI JSON
Download the OpenAPI specification at http://localhost:8000/openapi.json

## Error Handling

The API returns structured error responses:

### Validation Error (422)
```json
{
  "error": "Validation Error",
  "detail": "Invalid input data",
  "errors": [
    {
      "field": "player1_id",
      "message": "field required",
      "type": "value_error.missing"
    }
  ]
}
```

### Not Found (404)
```json
{
  "detail": "Player with id 999 not found"
}
```

### Conflict (409)
```json
{
  "error": "Integrity Error",
  "detail": "Resource with this value already exists"
}
```

### Internal Server Error (500)
```json
{
  "error": "Internal Server Error",
  "detail": "An unexpected error occurred"
}
```

## Database Views

The statistics endpoints use optimized PostgreSQL views:

- **player_statistics** - Aggregates match results by player
- **deck_statistics** - Aggregates match results by deck
- **deck_matchups** - Head-to-head deck performance
- **match_results** - Computed match winners from games

These views are defined in `../database/03_views.sql`.

## Performance Considerations

- **Connection Pooling**: SQLAlchemy manages 10-20 database connections
- **Indexes**: Optimized for common queries (see `../database/02_indexes.sql`)
- **Batch Operations**: Use `/api/v1/matches/batch` for bulk inserts
- **Pagination**: All list endpoints support `skip` and `limit` parameters

## Development

### Running Tests

```bash
# Install test dependencies
pip install pytest pytest-cov httpx

# Run tests
pytest
```

### Code Quality

```bash
# Install dev dependencies
pip install black flake8 mypy

# Format code
black app/

# Lint code
flake8 app/

# Type check
mypy app/
```

## Deployment

### Using Railway (Recommended)

This project is ready for Railway deployment with automatic configuration:

1. Push code to GitHub
2. Deploy from Railway dashboard
3. Railway automatically detects the `Procfile` and deploys

For detailed Railway deployment instructions, see [RAILWAY_DEPLOYMENT.md](../RAILWAY_DEPLOYMENT.md) in the root directory.

**Quick Setup:**
- Service uses `Procfile` for automatic deployment
- Set `DATABASE_URL` to Railway PostgreSQL connection string
- Set `CORS_ORIGINS` to your Streamlit frontend URL
- Railway automatically provides `$PORT` variable

### Using Docker

Create `Dockerfile`:

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY app/ ./app/

CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

Build and run:

```bash
docker build -t mtg-api .
docker run -p 8000:8000 --env-file .env mtg-api
```

### Environment Variables for Production

```ini
DATABASE_URL=postgresql://user:pass@db-host:5432/mtg_tournaments
SERVER_HOST=0.0.0.0
SERVER_PORT=8000
DEBUG=False
CORS_ORIGINS=https://yourdomain.com
```

## Troubleshooting

### Database Connection Error

```
OperationalError: could not connect to server
```

**Solution**: Check DATABASE_URL in `.env` and ensure PostgreSQL is running:

```bash
# Windows
pg_ctl status

# Check if database exists
psql -U postgres -l | grep mtg_tournaments
```

### Import Errors

```
ModuleNotFoundError: No module named 'app'
```

**Solution**: Ensure you're in the `services` directory and virtual environment is activated:

```bash
cd services
venv\Scripts\activate  # Windows
python -m app.main
```

### Port Already in Use

```
OSError: [WinError 10048] Only one usage of each socket address
```

**Solution**: Change port in `.env` or kill process using port 8000:

```bash
# Find process on port 8000
netstat -ano | findstr :8000

# Kill process (replace PID)
taskkill /PID <PID> /F
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Run tests and linting
5. Submit a pull request

## License

This project is provided as-is for tournament tracking purposes.

## Support

For issues or questions:
- Check the [API documentation](http://localhost:8000/docs)
- Review [EXAMPLES.md](EXAMPLES.md) for usage patterns
- Examine the database schema in `../database/01_schema.sql`

## Changelog

### Version 1.0.0
- Initial release
- Complete CRUD for all entities
- Statistics endpoints with database views
- Batch match insertion
- Automatic API documentation
- Error handling and validation
