from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.services.factory import factory_service
from backend.app.schemas.factory import Machine, MachineCreate
from backend.app.models.tenant import User
from backend.app.repositories.factory import machine_repo

router = APIRouter()

@router.get("/", response_model=List[Machine])
async def read_machines(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Basic tenant-aware list
    from sqlalchemy import select
    from backend.app.models.factory import Machine as MachineModel
    result = await db.execute(select(MachineModel).where(MachineModel.tenant_id == current_user.tenant_id, MachineModel.is_deleted == False))
    return result.scalars().all()

@router.post("/", response_model=Machine)
async def create_machine(
    *,
    db: AsyncSession = Depends(deps.get_db),
    machine_in: MachineCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await factory_service.create_machine(db, machine_in, current_user)
