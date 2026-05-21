from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.services.factory import factory_service
from backend.app.schemas.factory import Factory, FactoryCreate
from backend.app.models.tenant import User

router = APIRouter()

@router.get("/", response_model=List[Factory])
async def read_factories(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await factory_service.get_factories(db, current_user)

@router.post("/", response_model=Factory)
async def create_factory(
    *,
    db: AsyncSession = Depends(deps.get_db),
    factory_in: FactoryCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await factory_service.create_factory(db, factory_in, current_user)
