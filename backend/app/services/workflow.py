from typing import List, Any, Optional
from uuid import UUID
from datetime import datetime, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.models.workflow import ShiftHandover, Shift
from backend.app.models.downtime import DowntimeEvent
from backend.app.schemas.workflow import ShiftHandoverCreate, ShiftCreate
from backend.app.models.tenant import User

class WorkflowService:
    async def create_shift(self, db: AsyncSession, obj_in: ShiftCreate, user: User) -> Shift:
        db_obj = Shift(
            **obj_in.model_dump(),
            tenant_id=user.tenant_id
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_handover(self, db: AsyncSession, obj_in: ShiftHandoverCreate, user: User) -> ShiftHandover:
        data = obj_in.model_dump(exclude={"carryover_event_ids"})
        data["tenant_id"] = user.tenant_id
        data["supervisor_id"] = user.id

        db_obj = ShiftHandover(**data)

        if obj_in.carryover_event_ids:
            result = await db.execute(select(DowntimeEvent).where(DowntimeEvent.id.in_(obj_in.carryover_event_ids)))
            db_obj.carryover_events = result.scalars().all()

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_handovers(self, db: AsyncSession, user: User) -> List[ShiftHandover]:
        from sqlalchemy import select
        result = await db.execute(
            select(ShiftHandover)
            .where(ShiftHandover.tenant_id == user.tenant_id, ShiftHandover.is_deleted == False)
            .order_by(ShiftHandover.date.desc())
        )
        return result.scalars().all()

workflow_service = WorkflowService()
