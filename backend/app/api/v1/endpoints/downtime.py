from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.services.downtime import downtime_service
from backend.app.repositories.downtime import downtime_repo
from backend.app.schemas.downtime import DowntimeEvent, DowntimeEventCreate, DowntimeEventUpdate
from backend.app.models.tenant import User
from backend.app.models.downtime import DowntimeStatus
import uuid

router = APIRouter()

@router.get("/", response_model=List[DowntimeEvent])
async def read_downtime_events(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    status: Optional[DowntimeStatus] = None,
    line_id: Optional[uuid.UUID] = Query(None, alias="lineId"),
    skip: int = 0,
    limit: int = 100
) -> Any:
    return await downtime_repo.list_filtered(
        db,
        tenant_id=current_user.tenant_id,
        status=status,
        production_line_id=line_id,
        skip=skip,
        limit=limit
    )

@router.get("/{event_id}", response_model=DowntimeEvent)
async def read_downtime_event(
    event_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    event = await downtime_repo.get_with_details(db, id=event_id, tenant_id=current_user.tenant_id)
    if not event:
        raise HTTPException(status_code=404, detail="Downtime event not found")
    return event

@router.post("/", response_model=DowntimeEvent)
async def create_downtime_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_in: DowntimeEventCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await downtime_service.create_event(db, obj_in=event_in, user=current_user)

@router.patch("/{event_id}", response_model=DowntimeEvent)
async def update_downtime_event(
    *,
    db: AsyncSession = Depends(deps.get_db),
    event_id: uuid.UUID,
    event_in: DowntimeEventUpdate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    event = await downtime_service.update_event(db, event_id=event_id, obj_in=event_in, user=current_user)
    if not event:
        raise HTTPException(status_code=404, detail="Downtime event not found")
    return event
