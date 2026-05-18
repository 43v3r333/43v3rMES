from fastapi import APIRouter, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import text
from backend.app.api import deps
import redis.asyncio as redis
from backend.app.core.config import settings

router = APIRouter()

@router.get("/")
async def health_check():
    return {"status": "healthy"}

@router.get("/db")
async def db_health(db: AsyncSession = Depends(deps.get_db)):
    try:
        await db.execute(text("SELECT 1"))
        return {"status": "healthy", "service": "database"}
    except Exception as e:
        return {"status": "unhealthy", "service": "database", "detail": str(e)}

@router.get("/redis")
async def redis_health():
    try:
        r = redis.from_url(settings.REDIS_URL)
        await r.ping()
        return {"status": "healthy", "service": "redis"}
    except Exception as e:
        return {"status": "unhealthy", "service": "redis", "detail": str(e)}
