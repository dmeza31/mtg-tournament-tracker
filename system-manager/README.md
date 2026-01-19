# System Manager - CRUD Management Application

## Overview
The System Manager is a dedicated Streamlit application for CRUD (Create, Read, Update, Delete) operations on core tournament entities:
- **Seasons**: Create, search, and update tournament seasons
- **Tournaments**: Organize tournaments with search by name and location
- **Matches**: Create and manage matches with search by tournament and player

## Quick Start - Local Development

### Prerequisites
- Python 3.9+
- Virtual environment configured
- FastAPI backend running on port 8000

### Running Locally

```bash
cd "MTG Tournament Tracker"
.\.venv\Scripts\activate  # Windows
streamlit run system-manager/app.py
```

Access at `http://localhost:8501`

**Environment Variables (Local):**
```bash
# Optional - defaults to localhost
export API_BASE_URL="http://localhost:8000/api/v1"
```

## Quick Start - Railway Deployment

### Prerequisites
- Railway account
- GitHub repository synced with Railway

### Deployment

1. **Add Environment Variable:**
   ```
   API_BASE_URL=https://your-api-domain.railway.app/api/v1
   ```

2. **Deploy with Procfile:**
   ```bash
   web: streamlit run system-manager/app.py --server.port $PORT --server.address 0.0.0.0
   ```

3. **Or create new Railway service:**
   - Start Command: `streamlit run system-manager/app.py --server.port $PORT --server.address 0.0.0.0`

## Features

### 📅 Seasons
- **Search**: By partial name matching
- **Create**: Add new seasons with date ranges
- **Update**: Modify existing season details

### 🏆 Tournaments
- **Search**: By name (partial) AND location (partial)
- **Create**: New tournaments within seasons
- **Update**: Tournament details (name, location, format, date)

### 🎮 Matches
- **Search**: By tournament name and/or player name
- **Create**: New matches with player/tournament selection
- **Update**: Match details (round number, etc.)

## Configuration

The app auto-detects environment:
- **Local**: Uses `http://localhost:8000/api/v1` by default
- **Railway**: Uses `API_BASE_URL` environment variable

## API Endpoints Used

- `GET /seasons` - List all seasons
- `POST /seasons` - Create season
- `PUT /seasons/{id}` - Update season
- `GET /tournaments` - List tournaments
- `POST /tournaments` - Create tournament
- `PUT /tournaments/{id}` - Update tournament
- `GET /matches` - List matches
- `POST /matches` - Create match
- `PUT /matches/{id}` - Update match
- `GET /players` - List players
- `GET /health` - Health check

## Troubleshooting

### Cannot Connect to API
- **Local**: Verify FastAPI runs on port 8000: `curl http://localhost:8000/api/v1/health`
- **Railway**: Check `API_BASE_URL` matches your API service: `curl $API_BASE_URL/health`

### Search Returns No Results
- Verify data exists in database
- Try shorter/broader search terms
- Check main dashboard to confirm data is present

### Form Submission Fails
- Check browser console (F12) for error details
- Verify required fields are filled
- Test API endpoint directly: `curl {API_BASE_URL}/health`

## Development

### File Structure
```
system-manager/
├── app.py              # Main Streamlit application
├── README.md           # This file
└── requirements.txt    # Python dependencies (optional, shares with parent)
```

### Adding New Tabs
```python
# In main() function
tab4 = st.tabs([..., "New Feature"])
with tab4:
    render_new_feature()  # Create render function

# Add render function
def render_new_feature():
    st.header("🆕 New Feature")
    # Add UI components
```

## Related Documentation
- Main Dashboard: [UI/README.md](../UI/README.md)
- API Backend: [services/README.md](../services/README.md)
- Database: [database/README.md](../database/README.md)
- Tournament Import: [UI/CRUD_MANAGEMENT_GUIDE.md](../UI/CRUD_MANAGEMENT_GUIDE.md)
