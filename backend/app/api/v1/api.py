from fastapi import APIRouter
from backend.app.api.v1.endpoints import auth, factories, machines, downtime, workflow

api_router = APIRouter()
api_router.include_router(auth.router, prefix="/auth", tags=["auth"])
api_router.include_router(factories.router, prefix="/factories", tags=["factories"])
api_router.include_router(machines.router, prefix="/machines", tags=["machines"])
api_router.include_router(downtime.router, prefix="/downtime-events", tags=["downtime"])
api_router.include_router(workflow.router, tags=["workflow"])
