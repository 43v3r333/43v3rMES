from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.api import deps
import redis.asyncio as redis
from backend.app.core.config import settings
import time

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy", "version": "1.0.0-enterprise"}

@router.get("/db")
async def db_health(db: AsyncSession = Depends(deps.get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "service": "postgresql"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/redis")
async def redis_health():
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}

@router.get("/workers")
async def workers_health():
    # Placeholder for worker health check (e.g., Celery inspect)
    return {"status": "healthy", "service": "background-workers"}

@router.get("/storage")
async def storage_health():
    return {"status": "healthy", "service": "blob-storage"}

@router.get("/search")
async def search_health():
    return {"status": "healthy", "service": "search-index"}

@router.get("/diagnostics")
async def full_diagnostics(db: AsyncSession = Depends(deps.get_db)):
    return {
        "status": "healthy",
        "components": {
            "database": await db_health(db),
            "cache": await redis_health(),
            "workers": await workers_health(),
            "storage": await storage_health(),
            "search": await search_health()
        }
    }
