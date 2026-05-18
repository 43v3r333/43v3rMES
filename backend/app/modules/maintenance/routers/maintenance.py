from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.maintenance.services.maintenance_service import maintenance_service
from backend.app.modules.maintenance.repositories.maintenance_repo import wo_repo, pm_repo
from backend.app.modules.maintenance.schemas.maintenance import WorkOrder, WorkOrderCreate, WorkOrderUpdate, PMSchedule
from backend.app.models.tenant import User
from backend.app.modules.maintenance.models.maintenance import WorkOrderStatus
import uuid

router = APIRouter()

@router.get("/work-orders", response_model=List[WorkOrder])
async def read_work_orders(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    status: Optional[WorkOrderStatus] = None,
) -> Any:
    return await wo_repo.get_by_tenant(db, current_user.tenant_id, status=status)

@router.post("/work-orders", response_model=WorkOrder)
async def create_work_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    wo_in: WorkOrderCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await maintenance_service.create_work_order(db, wo_in, current_user)

@router.patch("/work-orders/{wo_id}", response_model=WorkOrder)
async def update_work_order(
    *,
    db: AsyncSession = Depends(deps.get_db),
    wo_id: uuid.UUID,
    wo_in: WorkOrderUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    wo = await maintenance_service.update_work_order(db, wo_id, wo_in, current_user)
    if not wo:
        raise HTTPException(status_code=404, detail="Work order not found")
    return wo

@router.get("/preventive-maintenance", response_model=List[PMSchedule])
async def read_pm_schedules(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await pm_repo.get_active_by_tenant(db, current_user.tenant_id)
