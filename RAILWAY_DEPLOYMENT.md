# Railway Deployment Guide

This guide walks you through deploying the MTG Tournament Tracker system to Railway with three services: PostgreSQL database, FastAPI backend, and Streamlit frontend.

## Architecture Overview

```
Railway Project
├── PostgreSQL Database (Railway Plugin)
├── FastAPI Backend Service
└── Streamlit UI Service
```

## Prerequisites

1. **Railway Account** - Sign up at [railway.app](https://railway.app)
2. **GitHub Repository** (recommended) - Push your code to GitHub for automatic deployments
3. **Railway CLI** (optional) - Install via `npm i -g @railway/cli`

## Deployment Steps

### Step 1: Create Railway Project

1. Log in to [Railway Dashboard](https://railway.app/dashboard)
2. Click **"New Project"**
3. Select **"Deploy from GitHub repo"** (or **"Empty Project"** if deploying manually)

### Step 2: Add PostgreSQL Database

1. In your Railway project, click **"+ New"**
2. Select **"Database"** → **"Add PostgreSQL"**
3. Railway automatically provisions a PostgreSQL instance and sets the `DATABASE_URL` variable
4. Note the database service name (e.g., `postgres`)

### Step 3: Initialize Database Schema

After PostgreSQL is provisioned, you need to run the initialization scripts:

#### Option A: Using Railway CLI (Recommended)

```bash
# Install Railway CLI
npm i -g @railway/cli

# Login to Railway
railway login

# Link to your project
railway link

# Run initialization script
cd database
railway run bash init.sh
```

#### Option B: Using psql Directly

1. Get the DATABASE_URL from Railway:
   - Go to PostgreSQL service → **Variables** tab
   - Copy the `DATABASE_URL` value

2. Run from your local machine:
```bash
cd database

# Set DATABASE_URL
export DATABASE_URL="postgresql://postgres:password@host:port/railway"  # Replace with your URL

# Execute scripts
psql $DATABASE_URL -f 01_schema.sql
psql $DATABASE_URL -f 02_indexes.sql
psql $DATABASE_URL -f 03_views.sql
```

#### Option C: Manual via Railway Dashboard

1. Open PostgreSQL service → **Data** tab
2. Use the built-in query editor to copy/paste contents of:
   - `01_schema.sql`
   - `02_indexes.sql`
   - `03_views.sql`

### Step 4: Deploy FastAPI Backend

1. In your Railway project, click **"+ New"** → **"GitHub Repo"** (or **"Empty Service"**)
2. Select your repository
3. Configure the service:

   **Settings:**
   - **Root Directory**: `services`
   - **Start Command**: (Auto-detected from `Procfile`)
   
   **Environment Variables:**
   ```bash
   DATABASE_URL=${{postgres.DATABASE_URL}}  # Reference to PostgreSQL service
   SERVER_HOST=0.0.0.0
   SERVER_PORT=$PORT  # Railway provides this automatically
   CORS_ORIGINS=*  # Update after deploying frontend
   DEBUG=False
   APP_NAME=MTG Tournament Tracker API
   APP_VERSION=1.0.0
   ```

4. Click **"Deploy"**
5. Once deployed, note the public URL (e.g., `https://your-api.up.railway.app`)

### Step 5: Deploy Streamlit Frontend

1. In your Railway project, click **"+ New"** → **"GitHub Repo"** (or **"Empty Service"**)
2. Select your repository
3. Configure the service:

   **Settings:**
   - **Root Directory**: `UI`
   - **Start Command**: (Auto-detected from `Procfile`)
   
   **Environment Variables:**
   ```bash
   API_BASE_URL=https://your-api.up.railway.app/api/v1  # Use your FastAPI URL from Step 4
   ```

4. Click **"Deploy"**
5. Once deployed, note the public URL (e.g., `https://your-app.up.railway.app`)

### Step 6: Update CORS Configuration

Now that you have the Streamlit frontend URL, update the FastAPI backend:

1. Go to **FastAPI Backend Service** → **Variables**
2. Update `CORS_ORIGINS`:
   ```bash
   CORS_ORIGINS=https://your-app.up.railway.app
   ```
3. Service will automatically redeploy with new CORS settings

## Environment Variables Reference

### PostgreSQL Service
No configuration needed - Railway manages automatically.

**Generated Variables:**
- `DATABASE_URL` - Connection string (referenced by FastAPI)
- `PGHOST`, `PGPORT`, `PGUSER`, `PGPASSWORD`, `PGDATABASE` - Individual components

### FastAPI Backend Service

| Variable | Value | Description |
|----------|-------|-------------|
| `DATABASE_URL` | `${{postgres.DATABASE_URL}}` | Reference to PostgreSQL service |
| `SERVER_HOST` | `0.0.0.0` | Listen on all interfaces |
| `SERVER_PORT` | `$PORT` | Railway's dynamic port (auto-provided) |
| `CORS_ORIGINS` | `https://your-app.up.railway.app` | Streamlit frontend URL |
| `DEBUG` | `False` | Disable debug mode in production |
| `APP_NAME` | `MTG Tournament Tracker API` | Optional application name |
| `APP_VERSION` | `1.0.0` | Optional version string |

### Streamlit UI Service

| Variable | Value | Description |
|----------|-------|-------------|
| `API_BASE_URL` | `https://your-api.up.railway.app/api/v1` | FastAPI backend URL with /api/v1 path |

## Service Dependencies

Configure service dependencies to ensure proper startup order:

1. **FastAPI Backend** depends on **PostgreSQL**
   - Go to FastAPI service → **Settings** → **Service Dependencies**
   - Add dependency on PostgreSQL service

2. **Streamlit UI** depends on **FastAPI Backend**
   - Go to Streamlit service → **Settings** → **Service Dependencies**
   - Add dependency on FastAPI service

## Monitoring & Logs

### View Logs
- Click on any service → **Deployments** → Select deployment → **View Logs**

### Health Checks
- **FastAPI**: `https://your-api.up.railway.app/health`
- **API Docs**: `https://your-api.up.railway.app/docs`

### Metrics
- Railway dashboard shows CPU, Memory, and Network usage per service

## Local Testing with Production URLs

You can test Railway services locally:

```bash
# Test FastAPI backend
curl https://your-api.up.railway.app/health

# Run Streamlit locally pointing to Railway API
cd UI
export API_BASE_URL="https://your-api.up.railway.app/api/v1"
streamlit run streamlit_app.py
```

## Troubleshooting

### Database Connection Errors

**Symptom:** FastAPI fails to connect to PostgreSQL

**Solution:**
- Verify `DATABASE_URL` variable references PostgreSQL: `${{postgres.DATABASE_URL}}`
- Check PostgreSQL service is running
- Ensure service dependency is configured

### CORS Errors in Browser

**Symptom:** Frontend shows CORS policy errors

**Solution:**
- Update `CORS_ORIGINS` in FastAPI service with exact Streamlit URL
- Include protocol: `https://your-app.up.railway.app` (not `http://`)
- No trailing slash

### Port Binding Errors

**Symptom:** Service fails with "Address already in use"

**Solution:**
- Ensure `Procfile` uses `$PORT` variable
- Railway dynamically assigns ports - don't hardcode port numbers

### Database Schema Not Found

**Symptom:** API returns "relation does not exist" errors

**Solution:**
- Run database initialization scripts (see Step 3)
- Verify scripts executed successfully by checking PostgreSQL logs

### Streamlit Can't Reach API

**Symptom:** Streamlit shows connection errors

**Solution:**
- Verify `API_BASE_URL` includes `/api/v1` path
- Test FastAPI health endpoint directly: `https://your-api.up.railway.app/health`
- Check FastAPI service is deployed and running

## Automatic Deployments

Railway automatically redeploys when you push to GitHub:

1. **Enable Auto-Deploy:**
   - Service → **Settings** → **Source**
   - Enable **"Deploy on push"**

2. **Branch Configuration:**
   - Choose branch to deploy (e.g., `main` or `production`)

3. **Deploy Triggers:**
   - Push to GitHub triggers automatic build and deployment
   - View deployment progress in Railway dashboard

## Database Backups

Railway PostgreSQL includes automatic backups:

1. Go to **PostgreSQL service** → **Backups**
2. Manual backup: Click **"Create Backup"**
3. Restore: Select backup → **"Restore"**

## Cost Optimization

Railway offers:
- **Hobby Plan**: $5/month base + usage
- **Free Trial**: $5 credit for testing

**Tips:**
- Use sleep mode for non-production environments
- Monitor usage in billing dashboard
- Scale down during low-traffic periods

## Custom Domains (Optional)

Add custom domains to your services:

1. Service → **Settings** → **Networking**
2. Click **"Generate Domain"** or **"Custom Domain"**
3. Configure DNS records as instructed

## Production Checklist

- [ ] Database initialized with schema, indexes, and views
- [ ] FastAPI backend deployed and accessible
- [ ] Streamlit frontend deployed and accessible
- [ ] CORS configured with correct frontend URL
- [ ] Service dependencies configured
- [ ] Environment variables verified
- [ ] Health endpoints responding
- [ ] Database backups enabled
- [ ] Logs monitored for errors
- [ ] API documentation accessible at `/docs`

## Local Development Compatibility

All deployment changes are **backwards compatible** with local development:

```bash
# Local FastAPI (still works)
cd services
python -m app.main

# Local Streamlit (still works)
cd UI
streamlit run streamlit_app.py

# Environment variables fallback to localhost defaults
```

The `Procfile` files are only used by Railway and don't affect local development.

## Support

- **Railway Documentation**: https://docs.railway.app
- **Railway Discord**: https://discord.gg/railway
- **MTG Tracker API Docs**: `https://your-api.up.railway.app/docs`

## Next Steps

After deployment:
1. Test all API endpoints via Swagger UI
2. Create initial season, tournaments, and players via Streamlit
3. Set up monitoring and alerts
4. Configure custom domain (optional)
5. Enable automatic backups schedule

---

**Deployment Complete!** 🚀

Access your application:
- **Streamlit UI**: `https://your-app.up.railway.app`
- **API**: `https://your-api.up.railway.app`
- **API Docs**: `https://your-api.up.railway.app/docs`
