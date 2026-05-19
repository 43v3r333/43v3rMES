#!/bin/bash
set -e

echo "Starting 43v3rMES Bootstrap..."

# Install dependencies
echo "Installing backend dependencies..."
pip install -r backend/requirements.txt

echo "Installing frontend dependencies..."
cd frontend && npm install && cd ..

# Setup environment
if [ ! -f .env ]; then
    echo "Initializing .env from .env.example..."
    cp .env.example .env
fi

# Apply migrations
echo "Applying database migrations..."
# cd backend && alembic upgrade head && cd ..

# Seed data (optional/prompt)
echo "Seeding demo data..."
export PYTHONPATH=$PYTHONPATH:.
# python scripts/seed_demo_data.py

echo "Bootstrap complete! You can now start the services."
