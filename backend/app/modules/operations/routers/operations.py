from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.operations.services.operations_service import operations_service
from backend.app.modules.operations.schemas.operations import OperationsOverview, ActiveIncident, MachineStatus
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/overview", response_model=OperationsOverview)
async def get_overview(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await operations_service.get_overview(db, current_user.tenant_id)

@router.get("/active-incidents", response_model=List[ActiveIncident])
async def get_active_incidents(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await operations_service.get_active_incidents(db, current_user.tenant_id)

@router.get("/machine-status", response_model=List[MachineStatus])
async def get_machine_status(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Logic to map machines to current status based on active downtime events
    return []
