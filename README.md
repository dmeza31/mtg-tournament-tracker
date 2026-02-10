# MTG Tournament Tracker

A comprehensive full-stack application for tracking Magic the Gathering tournament matches, player performance, deck statistics, and season standings with a modern web interface.

## Overview

The MTG Tournament Tracker is a complete tournament management system consisting of four main components:

1. **PostgreSQL Database** - Robust schema with optimized views for statistics
2. **FastAPI REST API** - High-performance backend with automatic documentation
3. **System Manager (Streamlit)** - Admin UI for CRUD operations and tournament import
4. **Streamlit Dashboard** - Read-only web interface for data visualization

## Architecture

```
┌─────────────────────────────────────────────────────────────┐
│                    MTG Tournament Tracker                    │
└─────────────────────────────────────────────────────────────┘

┌──────────────────┐      ┌──────────────────┐      ┌──────────────────┐
│   Streamlit UI   │ ───> │  FastAPI Backend │ ───> │   PostgreSQL DB  │
│   (Port 8501)    │ HTTP │   (Port 8000)    │ SQL  │   (Port 5432)    │
└──────────────────┘      └──────────────────┘      └──────────────────┘
    Frontend                   REST API                  Database
    - Season standings         - CRUD operations         - Core tables
    - Deck statistics          - Statistics endpoints    - Optimized views
    - Tournament results       - Batch operations        - Indexes
    - Matchup analysis         - Auto documentation      - Constraints
```

System Manager (admin Streamlit app) follows the same flow: Streamlit → FastAPI → PostgreSQL for CRUD and imports.

### Data Flow

1. **User Interaction** → Streamlit UI (read-only) and System Manager (admin) provide interactive forms and visualizations
2. **API Requests** → Both frontends communicate with the FastAPI backend via REST endpoints
3. **Database Operations** → FastAPI queries PostgreSQL using SQLAlchemy ORM
4. **Statistics** → Pre-built database views aggregate data for fast analytics
5. **Response** → Data flows back through API to the frontends for display

## Components

### 📊 Database (`database/`)

PostgreSQL database with comprehensive schema for tournament tracking:

- **Tables**: seasons, tournaments, players, deck_archetypes, matches, games
- **Views**: player_statistics, deck_statistics, deck_matchups, season_standings
- **Features**: Foreign key constraints, optimized indexes, cascade deletes

**Key Features:**
- Best-of-3 match tracking with individual game results
- Deck archetype management with color identity
- Season-based tournament organization
- Automatic win/draw/loss aggregation via views

[📖 Database Documentation](database/README.md)

### 🚀 Backend API (`services/`)

Python FastAPI application providing RESTful endpoints:

- **Framework**: FastAPI with Pydantic validation
- **ORM**: SQLAlchemy for database operations
- **Documentation**: Auto-generated Swagger UI and ReDoc
- **Features**: CORS support, error handling, batch operations

**Available Endpoints:**
- CRUD operations for all entities (seasons, tournaments, players, decks, matches)
- Statistics endpoints (player stats, deck stats, matchups, season standings)
- Batch match insertion with transaction support
- Health checks and API info

[📖 API Documentation](services/README.md)

### 🛠️ System Manager (`system-manager/`)

Streamlit admin console for CRUD and tournament imports:

- **CRUD**: Manage seasons, tournaments, matches, games, tournament types
- **Editing**: Update match players, game winners/results, and add games
- **Imports**: Upload a full tournament JSON via the 📤 Import tab (uses `/tournaments/import-complete`)
- **Dropdown tooling**: Player/tournament selectors to prevent typos

Run locally with `streamlit run system-manager/app.py`.

### 🎨 Frontend Dashboard (`UI/`)

Streamlit web application for data visualization:

- **Framework**: Streamlit with Plotly charts
- **Features**: Interactive dashboards, real-time data updates
- **Pages**: Season standings, deck statistics, tournament results

**Dashboard Features:**
- 🏆 **Season Standings**: Rankings with points system (3 per win, 1 per draw)
- 🎴 **Deck Analytics**: Win rates, meta analysis, matchup breakdowns
- 📊 **Tournament Results**: Round-by-round match and game details
- 🔍 **Deck Filter**: Analyze specific deck matchups with visual charts
- _(Import lives in System Manager; this UI is read-only for analytics.)_

[📖 UI Documentation](UI/README.md)

## Quick Start

### Prerequisites

- **Python 3.9+** - [Download](https://www.python.org/downloads/)
- **PostgreSQL 12+** - [Download](https://www.postgresql.org/download/)
- **Git** - For cloning the repository

### Local Development Setup

### Mac OSX setup

You may get this error:

- psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  role "postgres" does not exist

or 

- psql: error: connection to server on socket "/tmp/.s.PGSQL.5432" failed: FATAL:  database "your-username" does not exist



On your macOS/Homebrew setup, Postgres 10 didn’t:

- automatically create the postgres role 
- a matching database

So commands using -U postgres or defaulting to your OS username failed.



# Optional: You may have to install postgres15

```bash
# Binary is a different location on mac, include it in the path after installing it if you choose to use postgres15

echo 'export PATH="/opt/homebrew/opt/postgresql@15/bin:$PATH"' >> ~/.zshrc

source ~/.zshrc

# Verify Installation works 

psql —version

psql (PostgreSQL) 15.15 (Homebrew)
```


### Fix FATAL:  role "postgres" does not exist

Create the database and the role so the following command works:  psql -U postgres -d mtg_tournaments -f 01_schema.sql

```bash

# Get into the shell to create the role and the db

psql postgres

# Create role

CREATE ROLE postgres
WITH LOGIN SUPERUSER PASSWORD 'postgres';

SELECT datname FROM pg_database WHERE datname = 'mtg_tournaments';

# Create db

CREATE DATABASE mtg_tournaments;

ALTER DATABASE mtg_tournaments OWNER TO postgres;

# Exit  

Ctrl D 


Verify that it worked

# Get in to the mtg_tournaments that you created

psql  mtg_tournaments 

# Verify it works

\du

Ouput shows mtg_tournament tables
```

#### 1. Database Setup

```bash
# Create database
createdb mtg_tournaments

# Navigate to database folder
cd database

# Run initialization scripts
psql -U postgres -d mtg_tournaments -f 01_schema.sql
psql -U postgres -d mtg_tournaments -f 02_indexes.sql
psql -U postgres -d mtg_tournaments -f 03_views.sql

# Optional: Load sample data
psql -U postgres -d mtg_tournaments -f 05_sample_data.sql
```

#### 2. API Backend Setup

```bash
# Navigate to services folder
cd ../services

# Create virtual environment
python -m venv venv
venv\Scripts\activate  # Windows
# source venv/bin/activate  # Mac/Linux

# Install dependencies
pip install -r requirements.txt

# Configure environment
copy .env.example .env
# Edit .env with your database credentials

# Run API server
python -m app.main
```

API will be available at:
- **API**: http://localhost:8000
- **Swagger Docs**: http://localhost:8000/docs

#### 3. Streamlit UI Setup

```bash
# Open new terminal, navigate to UI folder
cd ../UI

# Install dependencies (use same or new venv)
pip install -r requirements.txt

# Run Streamlit app
streamlit run streamlit_app.py
```

Dashboard will be available at: http://localhost:8501

#### 4. System Manager (Admin) Setup

```bash
# From repo root (or a new terminal)
streamlit run system-manager/app.py
# Use --server.port 8502 if the UI is already running on 8501
```

System Manager will default to: http://localhost:8501

## Technology Stack

| Layer | Technology | Purpose |
|-------|-----------|---------|
| **Frontend** | Streamlit 1.29+ | Interactive web dashboard |
| **Visualization** | Plotly 5.18+ | Charts and graphs |
| **Backend** | FastAPI 0.115+ | REST API framework |
| **ORM** | SQLAlchemy 2.0+ | Database abstraction |
| **Validation** | Pydantic 2.10+ | Data validation and serialization |
| **Database** | PostgreSQL 12+ | Relational database |
| **Server** | Uvicorn | ASGI server for FastAPI |
| **Language** | Python 3.9+ | Primary language |

## Project Structure

```
MTG Tournament Tracker/
├── database/                          # PostgreSQL database
│   ├── 01_schema.sql                 # Core tables schema
│   ├── 02_indexes.sql                # Performance indexes
│   ├── 03_views.sql                  # Statistics views
│   ├── 05_sample_data.sql            # Test data
│   ├── init.sh                       # Railway initialization script
│   └── README.md                     # Database documentation
│
├── services/                          # FastAPI backend
│   ├── app/
│   │   ├── main.py                   # Application entry point
│   │   ├── config.py                 # Environment configuration
│   │   ├── database.py               # Database connection
│   │   ├── models.py                 # SQLAlchemy models
│   │   ├── schemas.py                # Pydantic schemas
│   │   ├── crud/                     # Database operations
│   │   └── routers/                  # API endpoints
│   ├── .env.example                  # Environment template
│   ├── requirements.txt              # Python dependencies
│   ├── Procfile                      # Railway deployment config
│   └── README.md                     # API documentation
│
├── system-manager/                   # Admin Streamlit app (CRUD + import)
│   └── app.py                        # System Manager entrypoint
│
├── UI/                                # Streamlit frontend (read-only analytics)
│   ├── streamlit_app.py              # Main dashboard
│   ├── requirements.txt              # UI dependencies
│   ├── Procfile                      # Railway deployment config
│   └── README.md                     # UI documentation
│
├── imports/                          # Tournament import templates and samples
│   ├── IMPORT_FORMAT_REFERENCE.md    # Field reference for import JSON
│   ├── README.md                     # Import resources overview
│   ├── tournament_import_example.json
│   ├── tournament_import_template.json
│   └── DataImport/                   # Raw and cleaned sample data
│
├── RAILWAY_DEPLOYMENT.md             # Cloud deployment guide
└── README.md                         # This file
```

## Key Features

### Tournament Management
✅ **Season Organization** - Group tournaments by season with date ranges  
✅ **Tournament Creation** - Track multiple tournaments per season  
✅ **Player Registration** - Manage player profiles with active status  
✅ **Deck Archetypes** - Catalog decks with color identity and archetype type  
✅ **Tournament Types** - Configure per-event point values (default LGS Tournament)
✅ **Bulk Imports** - Create tournaments, players, decks, matches, and games from a JSON file (System Manager)

### Match Tracking
✅ **Best-of-3 Format** - Record individual game results within matches  
✅ **Batch Operations** - Insert multiple matches with games in one transaction  
✅ **Round Management** - Organize matches by tournament rounds  
✅ **Automatic Winners** - Match winners determined from game results  

### Statistics & Analytics
✅ **Player Statistics** - Win/draw/loss records and win rates  
✅ **Deck Performance** - Analyze deck archetype success rates  
✅ **Matchup Analysis** - Head-to-head deck performance data  
✅ **Season Standings** - Rankings with points (3 per win, 1 per draw)  

### User Experience
✅ **Interactive Dashboard** - Streamlit UI with responsive design  
✅ **Visual Analytics** - Plotly charts for data visualization  
✅ **Real-time Updates** - Refresh data on demand  
✅ **API Documentation** - Auto-generated Swagger UI for testing  

## Deployment

### Local Development
All components run independently on localhost (see Quick Start above)

### Cloud Deployment (Railway)
The system is ready for Railway deployment with automatic configuration:

- **Services**: PostgreSQL database, FastAPI backend, Streamlit frontend (UI), and optional System Manager admin app
- **Auto-deploy**: Procfiles for automatic service configuration
- **Environment Variables**: Pre-configured for production use
- **Service Dependencies**: Proper startup order and URL references

[📖 Railway Deployment Guide](RAILWAY_DEPLOYMENT.md)

## API Documentation

Once the API is running, access interactive documentation:

- **Swagger UI**: http://localhost:8000/docs - Interactive API testing
- **ReDoc**: http://localhost:8000/redoc - Clean API documentation
- **OpenAPI JSON**: http://localhost:8000/openapi.json - API specification

## Use Cases

### Tournament Organizers
- Create seasons and tournaments
- Register players and their deck choices
- Record match results round by round
- View real-time standings

### Players
- Check personal statistics and performance
- Compare deck matchup win rates
- Track season rankings and points

### Analysts
- Analyze meta game trends
- Identify top-performing decks
- Study matchup dynamics
- Export data via API

## Data Models

### Core Entities
- **Season** - Tournament season with start/end dates
- **Tournament** - Individual tournament event within a season
- **Player** - Player profile with contact information
- **Deck Archetype** - Deck type with color identity and strategy
- **Match** - Best-of-3 match between two players
- **Game** - Individual game result within a match

### Relationships
```
Season (1) ──< (N) Tournament
Tournament (1) ──< (N) Match
Player (1) ──< (N) Match (as player1 or player2)
Deck Archetype (1) ──< (N) Match (as deck1 or deck2)
Match (1) ──< (1-3) Game
```

## Performance

### Database Optimizations
- **Indexes** on foreign keys and commonly queried fields
- **Views** pre-aggregate statistics for fast queries
- **Connection Pooling** (10-20 connections) in SQLAlchemy
- **Cascade Deletes** maintain referential integrity

### API Performance
- **Async Operations** via FastAPI and Uvicorn
- **Batch Endpoints** for bulk insertions
- **Pagination Support** on list endpoints
- **Response Models** optimize JSON serialization

## Contributing

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/new-feature`)
3. Make your changes
4. Run tests and linting
5. Commit your changes (`git commit -am 'Add new feature'`)
6. Push to the branch (`git push origin feature/new-feature`)
7. Create a Pull Request

## Troubleshooting

### Database Connection Issues
- Verify PostgreSQL is running: `pg_ctl status`
- Check DATABASE_URL in `services/.env`
- Ensure database `mtg_tournaments` exists

### API Not Starting
- Activate virtual environment in services folder
- Install all requirements: `pip install -r requirements.txt`
- Check port 8000 is not in use

### UI Cannot Connect to API
- Ensure API is running on http://localhost:8000
- Check API_BASE_URL configuration
- Verify CORS_ORIGINS includes localhost in API `.env`

## License

This project is provided as-is for tournament tracking purposes.

## Support & Documentation

- **Database**: [database/README.md](database/README.md)
- **API**: [services/README.md](services/README.md) & [services/EXAMPLES.md](services/EXAMPLES.md)
- **System Manager**: Admin app at [system-manager/app.py](system-manager/app.py)
- **UI**: [UI/README.md](UI/README.md)
- **Imports**: [imports/README.md](imports/README.md) & [TOURNAMENT_IMPORT_GUIDE.md](TOURNAMENT_IMPORT_GUIDE.md)
- **Deployment**: [RAILWAY_DEPLOYMENT.md](RAILWAY_DEPLOYMENT.md)
- **API Testing**: http://localhost:8000/docs (when running)

## Roadmap

Future enhancements could include:
- User authentication and authorization
- Tournament bracket generation
- Swiss pairing algorithm
- Export functionality (CSV, Excel)
- Email notifications
- Mobile responsive design improvements
- Real-time updates via WebSockets

---

**Built with ❤️ for the Magic: The Gathering community**
