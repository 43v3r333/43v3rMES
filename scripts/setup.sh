#!/bin/bash
set -e

echo "Setting up AI MES Platform..."

# Check if .env exists
if [ ! -f .env ]; then
    echo "Creating .env from .env.example..."
    cp .env.example .env
fi

# Build and start containers
echo "Building and starting containers..."
docker-compose up -d --build

# Run migrations
echo "Running database migrations..."
docker-compose exec backend alembic upgrade head

echo "Setup complete! Access the platform at http://localhost"
