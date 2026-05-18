from datetime import datetime, timezone
from typing import List, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.downtime import DowntimeEvent, DowntimeStatus
from backend.app.models.factory import Machine
from backend.app.schemas.downtime import DowntimeEventCreate, DowntimeEventUpdate
from backend.app.models.tenant import User
from sqlalchemy import select

class DowntimeService:
    async def create_event(self, db: AsyncSession, obj_in: DowntimeEventCreate, user: User) -> DowntimeEvent:
        data = obj_in.model_dump(exclude={"machine_ids"})
        data["tenant_id"] = user.tenant_id
        data["reported_by"] = user.id
        data["created_by"] = user.id

        # Simple event number generation
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        data["event_number"] = f"DT-{timestamp}"

        # Calculate duration if ended_at is present
        if obj_in.ended_at:
            delta = obj_in.ended_at - obj_in.started_at
            data["duration_minutes"] = int(delta.total_seconds() / 60)

        db_obj = DowntimeEvent(**data)

        # Associate machines
        if obj_in.machine_ids:
            result = await db.execute(select(Machine).where(Machine.id.in_(obj_in.machine_ids)))
            db_obj.machines = result.scalars().all()

        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_event(self, db: AsyncSession, event_id: UUID, obj_in: DowntimeEventUpdate, user: User) -> Optional[DowntimeEvent]:
        # Implementation would include re-calculating duration if ended_at changes
        # and checking tenant isolation
        result = await db.execute(select(DowntimeEvent).where(DowntimeEvent.id == event_id, DowntimeEvent.tenant_id == user.tenant_id))
        db_obj = result.scalars().first()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        if "ended_at" in update_data or "started_at" in update_data:
            delta = db_obj.ended_at - db_obj.started_at
            db_obj.duration_minutes = int(delta.total_seconds() / 60)

        db_obj.updated_by = user.id
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

downtime_service = DowntimeService()
