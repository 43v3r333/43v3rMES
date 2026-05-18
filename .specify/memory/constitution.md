# Project Constitution: 43v3rMES

## Mission
To provide a production-grade AI-native Manufacturing Execution System (MES) SaaS platform for industrial operations.

## Tech Stack
- Frontend: Vue 3, TypeScript, Vite, TailwindCSS, Pinia, shadcn-vue, AG Grid.
- Backend: FastAPI, Python 3.12, SQLAlchemy, PostgreSQL, Alembic.
- Infrastructure: Docker, Docker Compose, Nginx.

## Architecture
- Multi-tenant hierarchy: Tenant > Factory > Area > Production Line > Machine.
- Repository pattern for data access.
- Soft delete and audit timestamps in all models.
- Enterprise layout shell with Dark Mode support.

## Guidelines
- No glassmorphism or neon styling.
- Compact enterprise spacing and typography.
- Modular architecture and reusable services.
