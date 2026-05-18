from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_, or_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.base import BaseRepository
from backend.app.modules.maintenance.models.maintenance import WorkOrder, WorkOrderStatus, PreventiveMaintenanceSchedule
from backend.app.modules.maintenance.schemas.maintenance import WorkOrderCreate, WorkOrderUpdate, PMScheduleCreate

class WorkOrderRepository(BaseRepository[WorkOrder, WorkOrderCreate, WorkOrderUpdate]):
    async def get_by_tenant(self, db: AsyncSession, tenant_id: UUID, status: Optional[WorkOrderStatus] = None) -> List[WorkOrder]:
        query = select(WorkOrder).where(WorkOrder.tenant_id == tenant_id, WorkOrder.is_deleted == False)
        if status:
            query = query.where(WorkOrder.status == status)
        result = await db.execute(query.order_by(WorkOrder.priority.desc(), WorkOrder.created_at.desc()))
        return result.scalars().all()

class PMRepository(BaseRepository[PreventiveMaintenanceSchedule, PMScheduleCreate, Any]):
    async def get_active_by_tenant(self, db: AsyncSession, tenant_id: UUID) -> List[PreventiveMaintenanceSchedule]:
        result = await db.execute(
            select(PreventiveMaintenanceSchedule).where(PreventiveMaintenanceSchedule.tenant_id == tenant_id, PreventiveMaintenanceSchedule.is_active == True)
        )
        return result.scalars().all()

wo_repo = WorkOrderRepository(WorkOrder)
pm_repo = PMRepository(PreventiveMaintenanceSchedule)
