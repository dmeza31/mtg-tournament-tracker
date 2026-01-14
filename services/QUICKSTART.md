# Quick Start Guide - MTG Tournament API

## 5-Minute Setup

### 1. Install Dependencies

```bash
cd services
python -m venv venv
venv\Scripts\activate
pip install -r requirements.txt
```

### 2. Configure Database

Create `.env` file:
```bash
copy .env.example .env
```

Edit `.env` with your PostgreSQL credentials:
```ini
DATABASE_URL=postgresql://postgres:your_password@localhost:5432/mtg_tournaments
```

### 3. Set Up Database (if not done already)

```bash
cd ..\database
psql -U postgres -d mtg_tournaments -f 01_schema.sql
psql -U postgres -d mtg_tournaments -f 02_indexes.sql
psql -U postgres -d mtg_tournaments -f 03_views.sql
psql -U postgres -d mtg_tournaments -f 05_sample_data.sql
```

### 4. Run the API

```bash
cd ..\services
python -m app.main
```

### 5. Open Swagger UI

Visit: **http://localhost:8000/docs**

## Quick Test

Open your browser or use curl:

```bash
# Health check
curl http://localhost:8000/health

# Get all players
curl http://localhost:8000/api/v1/players

# Get player statistics
curl http://localhost:8000/api/v1/stats/players
```

## Common Commands

### Start the server
```bash
python -m app.main
```

### With auto-reload (development)
```bash
uvicorn app.main:app --reload
```

### On different port
```bash
uvicorn app.main:app --port 8080
```

## Next Steps

1. **Read the full documentation**: [README.md](README.md)
2. **Try the examples**: [EXAMPLES.md](EXAMPLES.md)
3. **Explore Swagger UI**: http://localhost:8000/docs
4. **View ReDoc**: http://localhost:8000/redoc

## Troubleshooting

**Can't connect to database?**
- Check DATABASE_URL in `.env`
- Verify PostgreSQL is running: `pg_ctl status`

**Port already in use?**
- Change SERVER_PORT in `.env`
- Or kill process: `netstat -ano | findstr :8000`

**Import errors?**
- Activate virtual environment: `venv\Scripts\activate`
- Reinstall: `pip install -r requirements.txt`

## API Endpoints Summary

| Endpoint | Description |
|----------|-------------|
| `GET /health` | Health check |
| `GET /api/v1/seasons` | List seasons |
| `POST /api/v1/seasons` | Create season |
| `GET /api/v1/tournaments` | List tournaments |
| `POST /api/v1/tournaments` | Create tournament |
| `GET /api/v1/players` | List players |
| `POST /api/v1/players` | Create player |
| `GET /api/v1/decks` | List deck archetypes |
| `POST /api/v1/decks` | Create deck archetype |
| `GET /api/v1/matches` | List matches |
| `POST /api/v1/matches` | Create match |
| `POST /api/v1/matches/batch` | **Batch create matches** |
| `GET /api/v1/stats/players` | Player statistics |
| `GET /api/v1/stats/decks` | Deck statistics |
| `GET /api/v1/stats/matchups` | Deck matchup analysis |

Full API documentation: http://localhost:8000/docs
