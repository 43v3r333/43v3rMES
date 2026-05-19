# 43v3rMES - Enterprise AI-Native MES SaaS Platform

A production-grade, AI-native Manufacturing Execution System (MES) designed for industrial multi-site operations.

## Architecture
- **Enterprise Hierarchy**: Organization > Region > Factory > Area > Line > Machine.
- **Backend**: FastAPI (Python 3.12), SQLAlchemy, PostgreSQL, Alembic, Redis.
- **Frontend**: Vue 3, TypeScript, TailwindCSS, Pinia, AG Grid, Apache ECharts.
- **Infrastructure**: Docker, Docker Compose, Nginx, GitHub Codespaces.

## Key Modules
- **Operations Command Center**: High-density operational monitoring workspace.
- **Downtime Engine**: Core incident management and escalation system.
- **Maintenance Management**: Work order execution and PM planning.
- **Operational Intelligence**: AI-driven shift summaries and risk analysis.
- **Shift Handover**: Cross-shift continuity and carryover tracking.
- **Reporting & Export**: Standardized industrial reporting and data exports.

## Getting Started

### 🚀 Launch in GitHub Codespaces
1. Open the repository in a new Codespace.
2. Wait for the `postCreateCommand` to complete (`scripts/bootstrap.sh`).
3. Services will start automatically.

### 🛠️ Local Setup
1. **Bootstrap**: Run `bash scripts/bootstrap.sh`.
2. **Infrastructure**: `docker-compose up -d`.
3. **Seed Data**: `export PYTHONPATH=$PYTHONPATH:. && python scripts/seed_demo_data.py`.

### 🔑 Demo Credentials
- **Role**: Enterprise Admin
- **Email**: `admin@43v3r.com`
- **Password**: `password123`

## Platform Foundations
- **Security**: JWT Auth, RBAC, strict tenant isolation.
- **Observability**: Structured logging, Correlation IDs, health diagnostics.
- **Performance**: Redis-based caching, optimized aggregation queries.

## Testing
- Backend: `pytest`
- Frontend: `npm run test` (Vitest setup placeholder)

---
© 2024 43v3r Industrial. All rights reserved.
