#!/bin/bash
# Database initialization script for Railway PostgreSQL
# Executes SQL scripts in the correct order to set up the MTG Tournament Tracker database

set -e  # Exit on error

echo "Starting database initialization..."

# Check if PGDATABASE is set (Railway provides this)
if [ -z "$DATABASE_URL" ]; then
    echo "Error: DATABASE_URL environment variable is not set"
    exit 1
fi

# Execute SQL scripts in order
echo "Creating schema..."
psql $DATABASE_URL -f 01_schema.sql

echo "Creating indexes..."
psql $DATABASE_URL -f 02_indexes.sql

echo "Creating views..."
psql $DATABASE_URL -f 03_views.sql

# Check if season standings view file exists (may be integrated into 03_views.sql)
if [ -f "06_season_standings_view.sql" ]; then
    echo "Creating season standings view..."
    psql $DATABASE_URL -f 06_season_standings_view.sql
fi

echo "Database initialization complete!"
echo "Note: Sample data (05_sample_data.sql) not loaded. Load manually if needed."
