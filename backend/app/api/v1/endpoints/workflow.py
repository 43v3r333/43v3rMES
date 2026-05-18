from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.services.workflow import workflow_service
from backend.app.repositories.workflow import shift_repo, handover_repo
from backend.app.schemas.workflow import Shift, ShiftCreate, ShiftHandover, ShiftHandoverCreate
from backend.app.models.tenant import User
import uuid

router = APIRouter()

# Shifts
@router.get("/shifts", response_model=List[Shift])
async def read_shifts(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await shift_repo.get_by_tenant(db, current_user.tenant_id)

@router.post("/shifts", response_model=Shift)
async def create_shift(
    *,
    db: AsyncSession = Depends(deps.get_db),
    shift_in: ShiftCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await workflow_service.create_shift(db, shift_in, current_user)

# Handovers
@router.get("/shift-handovers", response_model=List[ShiftHandover])
async def read_handovers(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await workflow_service.get_handovers(db, current_user)

@router.post("/shift-handovers", response_model=ShiftHandover)
async def create_handover(
    *,
    db: AsyncSession = Depends(deps.get_db),
    handover_in: ShiftHandoverCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await workflow_service.create_handover(db, handover_in, current_user)

@router.get("/shift-handovers/{handover_id}", response_model=ShiftHandover)
async def read_handover(
    handover_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    handover = await handover_repo.get_with_details(db, handover_id, current_user.tenant_id)
    if not handover:
        raise HTTPException(status_code=404, detail="Handover not found")
    return handover
