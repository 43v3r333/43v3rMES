#!/bin/bash
echo "Seeding initial enterprise data..."
# This would call a python script to seed roles, permissions, and admin user
docker-compose exec backend python -m app.utils.seed
