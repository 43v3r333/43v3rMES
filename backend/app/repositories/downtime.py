from typing import List, Optional, Any
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.repositories.base import BaseRepository
from backend.app.models.downtime import DowntimeEvent, DowntimeCategory, DowntimeStatus
from backend.app.schemas.downtime import (
    DowntimeEventCreate, DowntimeEventUpdate,
    DowntimeCategoryCreate
)

class DowntimeRepository(BaseRepository[DowntimeEvent, DowntimeEventCreate, DowntimeEventUpdate]):
    async def get_with_details(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> Optional[DowntimeEvent]:
        result = await db.execute(
            select(DowntimeEvent)
            .options(
                selectinload(DowntimeEvent.machines),
                selectinload(DowntimeEvent.category),
                selectinload(DowntimeEvent.comments)
            )
            .where(DowntimeEvent.id == id, DowntimeEvent.tenant_id == tenant_id, DowntimeEvent.is_deleted == False)
        )
        return result.scalars().first()

    async def list_filtered(
        self,
        db: AsyncSession,
        tenant_id: UUID,
        status: Optional[DowntimeStatus] = None,
        production_line_id: Optional[UUID] = None,
        skip: int = 0,
        limit: int = 100
    ) -> List[DowntimeEvent]:
        query = select(DowntimeEvent).where(DowntimeEvent.tenant_id == tenant_id, DowntimeEvent.is_deleted == False)

        if status:
            query = query.where(DowntimeEvent.status == status)
        if production_line_id:
            query = query.where(DowntimeEvent.production_line_id == production_line_id)

        result = await db.execute(query.order_by(DowntimeEvent.started_at.desc()).offset(skip).limit(limit))
        return result.scalars().all()

downtime_repo = DowntimeRepository(DowntimeEvent)
category_repo = BaseRepository[DowntimeCategory, DowntimeCategoryCreate, Any](DowntimeCategory)
