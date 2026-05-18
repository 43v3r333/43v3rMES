from datetime import datetime, timezone
from typing import List, Any, Optional
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.modules.maintenance.models.maintenance import WorkOrder, WorkOrderStatus
from backend.app.modules.maintenance.schemas.maintenance import WorkOrderCreate, WorkOrderUpdate
from backend.app.models.tenant import User

class MaintenanceService:
    async def create_work_order(self, db: AsyncSession, obj_in: WorkOrderCreate, user: User) -> WorkOrder:
        data = obj_in.model_dump()
        data["tenant_id"] = user.tenant_id
        data["created_by"] = user.id

        # Simple WO number generation
        timestamp = datetime.now().strftime("%Y%m%d%H%M")
        data["work_order_number"] = f"WO-{timestamp}"

        db_obj = WorkOrder(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def update_work_order(self, db: AsyncSession, wo_id: UUID, obj_in: WorkOrderUpdate, user: User) -> Optional[WorkOrder]:
        from sqlalchemy import select
        result = await db.execute(select(WorkOrder).where(WorkOrder.id == wo_id, WorkOrder.tenant_id == user.tenant_id))
        db_obj = result.scalars().first()
        if not db_obj:
            return None

        update_data = obj_in.model_dump(exclude_unset=True)
        for field in update_data:
            setattr(db_obj, field, update_data[field])

        if obj_in.status == WorkOrderStatus.COMPLETED:
            db_obj.completed_at = datetime.now(timezone.utc)
            db_obj.completed_by = user.id

        await db.commit()
        await db.refresh(db_obj)
        return db_obj

maintenance_service = MaintenanceService()
