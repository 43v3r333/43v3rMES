from typing import Optional, List, Any
from pydantic import BaseModel
import uuid
from datetime import datetime
from backend.app.modules.maintenance.models.maintenance import WorkOrderStatus, WorkOrderPriority, WorkOrderType

class WorkOrderBase(BaseModel):
    title: str
    description: Optional[str] = None
    machine_id: uuid.UUID
    priority: WorkOrderPriority = WorkOrderPriority.MEDIUM
    type: WorkOrderType = WorkOrderType.CORRECTIVE
    due_date: Optional[datetime] = None
    linked_downtime_event_id: Optional[uuid.UUID] = None

class WorkOrderCreate(WorkOrderBase):
    pass

class WorkOrderUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    status: Optional[WorkOrderStatus] = None
    priority: Optional[WorkOrderPriority] = None
    assigned_to: Optional[uuid.UUID] = None
    maintenance_notes: Optional[str] = None
    resolution_summary: Optional[str] = None
    completed_at: Optional[datetime] = None
    labor_hours: Optional[float] = None

class WorkOrder(WorkOrderBase):
    id: uuid.UUID
    work_order_number: str
    status: WorkOrderStatus
    assigned_to: Optional[uuid.UUID] = None
    created_by: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    class Config: from_attributes = True

class PMScheduleBase(BaseModel):
    name: str
    description: Optional[str] = None
    machine_id: uuid.UUID
    interval_days: Optional[int] = None
    runtime_threshold_hours: Optional[float] = None
    is_active: bool = True

class PMScheduleCreate(PMScheduleBase):
    pass

class PMSchedule(PMScheduleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    next_due_at: Optional[datetime] = None
    class Config: from_attributes = True

class MaintenanceHistoryItem(BaseModel):
    id: uuid.UUID
    machine_id: uuid.UUID
    work_order_id: Optional[uuid.UUID] = None
    action_taken: str
    performed_by: uuid.UUID
    timestamp: datetime
    duration_hours: Optional[float] = None
    class Config: from_attributes = True
