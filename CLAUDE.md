# 43v3rMES Development Guide

## Build & Test Commands
- Backend Tests: `export PYTHONPATH=$PYTHONPATH:. && pytest backend/tests/test_auth.py`
- Run Backend: `uvicorn backend.app.main:app --reload --port 8000`
- Frontend Dev: `cd frontend && npm run dev`

## Spec-Kit Commands
- Specify: `/.specify` (Use speckit templates in .specify/templates)
- Plan: `/.plan`
- Tasks: `/.tasks`
- Implement: `/.implement`

## Project Standards
- Python: FastAPI, Pydantic, SQLAlchemy, Repository pattern.
- Frontend: Vue 3, Tailwind, Pinia, Enterprise Layouts.
- Infrastructure: Docker, Nginx.
