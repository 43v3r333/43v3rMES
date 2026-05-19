from fastapi import APIRouter
from backend.app.api.v1.endpoints import auth, factories, machines, downtime, workflow
from backend.app.modules.analytics.routers import analytics
from backend.app.modules.notifications.routers import notifications
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(maintenance.router, tags=["maintenance"])
api_router.include_router(reporting.router, prefix="/reports", tags=["reporting"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
from backend.app.modules.operations.routers import operations
from backend.app.api.v1.endpoints import health
from backend.app.modules.search.routers import search
api_router.include_router(maintenance.router, tags=["maintenance"])
api_router.include_router(reporting.router, prefix="/reports", tags=["reporting"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
from backend.app.modules.maintenance.routers import maintenance
api_router.include_router(reporting.router, prefix="/reports", tags=["reporting"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
from backend.app.modules.reporting.routers import reporting
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
from backend.app.modules.intelligence.routers import intelligence
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
from backend.app.modules.enterprise.routers import enterprise

api_router = APIRouter()
api_router.include_router(health.router, prefix="/health", tags=["health"])
api_router.include_router(search.router, prefix="/search", tags=["search"])
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(factories.router, prefix="/factories", tags=["factories"])
api_router.include_router(machines.router, prefix="/machines", tags=["machines"])
api_router.include_router(downtime.router, prefix="/downtime-events", tags=["downtime"])
api_router.include_router(workflow.router, tags=["workflow"])
api_router.include_router(analytics.router, prefix="/analytics", tags=["analytics"])
api_router.include_router(notifications.router, prefix="/notifications", tags=["notifications"])
api_router.include_router(operations.router, prefix="/operations", tags=["operations"])
api_router.include_router(maintenance.router, tags=["maintenance"])
api_router.include_router(reporting.router, prefix="/reports", tags=["reporting"])
api_router.include_router(intelligence.router, prefix="/intelligence", tags=["intelligence"])
api_router.include_router(enterprise.router, prefix="/enterprise", tags=["enterprise"])
