import json
import functools
import logging
from typing import Any, Optional
import redis.asyncio as redis
from backend.app.core.config import settings

logger = logging.getLogger("app")

class CacheManager:
    def __init__(self):
        self.redis = redis.from_url(settings.REDIS_URL)

    async def get(self, key: str) -> Optional[Any]:
        data = await self.redis.get(key)
        return json.loads(data) if data else None

    async def set(self, key: str, value: Any, expire: int = 300):
        await self.redis.set(key, json.dumps(value), ex=expire)

cache = CacheManager()

def cached(expire: int = 300):
    def decorator(func):
        @functools.wraps(func)
        async def wrapper(*args, **kwargs):
            # Key generation based on func name and args
            key = f"cache:{func.__name__}:{str(args)}:{str(kwargs)}"
            try:
                cached_val = await cache.get(key)
                if cached_val is not None:
                    return cached_val
            except Exception as e:
                logger.warning(f"Cache get failed: {e}")

            result = await func(*args, **kwargs)

            try:
                await cache.set(key, result, expire=expire)
            except Exception as e:
                logger.warning(f"Cache set failed: {e}")

            return result
        return wrapper
    return decorator
