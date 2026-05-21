import time
import logging
import uuid
from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from backend.app.api.deps import get_current_user

logger = logging.getLogger("app")

class LoggingMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request: Request, call_next):
        correlation_id = request.headers.get("X-Correlation-ID", str(uuid.uuid4()))
        start_time = time.time()

        # We can't easily access Depends(get_current_user) in middleware before the route executes
        # but we can log the token if present

        response = await call_next(request)

        process_time = time.time() - start_time
        response.headers["X-Correlation-ID"] = correlation_id

        logger.info(
            f"CorrelationID: {correlation_id} "
            f"Method: {request.method} Path: {request.url.path} "
            f"Status: {response.status_code} Duration: {process_time:.4f}s"
        )
        return response
