# 43v3rMES Architecture

## Backend
- FastAPI with modular routers.
- Repository pattern for data access.
- SQLAlchemy (async) for ORM.
- Alembic for migrations.
- Soft delete support in all core models.

## Frontend
- Vue 3 with Composition API.
- TailwindCSS for utility-first styling.
- Pinia for state management.
- Enterprise Layout Shell with sidebar/topbar.
- Dark mode support built-in.

## Infrastructure
- Docker Compose orchestrating Postgres, FastAPI, Vue (Nginx), and an Nginx reverse proxy.
- Environment-based configuration.
