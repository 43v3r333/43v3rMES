from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload
from backend.app.repositories.base import BaseRepository
from backend.app.models.workflow import Shift, ShiftHandover, AuditEvent
from backend.app.schemas.workflow import ShiftCreate, ShiftHandoverCreate, AuditEventBase

class ShiftRepository(BaseRepository[Shift, ShiftCreate, Any]):
    async def get_by_tenant(self, db: AsyncSession, tenant_id: UUID) -> List[Shift]:
        result = await db.execute(select(Shift).where(Shift.tenant_id == tenant_id, Shift.is_deleted == False))
        return result.scalars().all()

class HandoverRepository(BaseRepository[ShiftHandover, ShiftHandoverCreate, Any]):
    async def get_with_details(self, db: AsyncSession, id: UUID, tenant_id: UUID) -> Optional[ShiftHandover]:
        result = await db.execute(
            select(ShiftHandover)
            .options(
                selectinload(ShiftHandover.carryover_events),
                selectinload(ShiftHandover.notes)
            )
            .where(ShiftHandover.id == id, ShiftHandover.tenant_id == tenant_id, ShiftHandover.is_deleted == False)
        )
        return result.scalars().first()

class AuditRepository:
    async def log_event(self, db: AsyncSession, event_in: AuditEvent, tenant_id: UUID, user_id: UUID):
        db_obj = AuditEvent(
            **event_in.model_dump(),
            tenant_id=tenant_id,
            user_id=user_id,
            timestamp=datetime.now(timezone.utc)
        )
        db.add(db_obj)
        await db.commit()

shift_repo = ShiftRepository(Shift)
handover_repo = HandoverRepository(ShiftHandover)
