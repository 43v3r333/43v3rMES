import logging
from fastapi import Request, HTTPException
from fastapi.responses import JSONResponse
from starlette.status import HTTP_500_INTERNAL_SERVER_ERROR

logger = logging.getLogger("app")

async def global_exception_handler(request: Request, exc: Exception):
    correlation_id = request.headers.get("X-Correlation-ID", "unknown")
    logger.error(f"CorrelationID: {correlation_id} - Unhandled exception: {str(exc)}", exc_info=True)

    return JSONResponse(
        status_code=HTTP_500_INTERNAL_SERVER_ERROR,
        content={
            "detail": "An internal enterprise system error occurred.",
            "correlation_id": correlation_id
        }
    )
