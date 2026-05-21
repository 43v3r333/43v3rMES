from sqlalchemy import Column, String, Integer, Float, Boolean, DateTime, ForeignKey, UUID, Enum as SQLEnum
from sqlalchemy.orm import relationship
import uuid
from enum import Enum
from backend.app.db.base_class import Base

class WorkOrderStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    COMPLETED = "COMPLETED"
    CANCELLED = "CANCELLED"

class WorkOrderPriority(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

class WorkOrderType(str, Enum):
    CORRECTIVE = "CORRECTIVE"
    PREVENTIVE = "PREVENTIVE"
    PREDICTIVE = "PREDICTIVE"
    PROJECT = "PROJECT"

class WorkOrder(Base):
    __tablename__ = "work_orders"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    work_order_number = Column(String, unique=True, index=True, nullable=False)
    title = Column(String, nullable=False)
    description = Column(String)
    machine_id = Column(UUID(as_uuid=True), ForeignKey("machines.id"), nullable=False, index=True)
    status = Column(SQLEnum(WorkOrderStatus), default=WorkOrderStatus.OPEN, nullable=False, index=True)
    priority = Column(SQLEnum(WorkOrderPriority), default=WorkOrderPriority.MEDIUM, nullable=False, index=True)
    type = Column(SQLEnum(WorkOrderType), default=WorkOrderType.CORRECTIVE, nullable=False, index=True)
    due_date = Column(DateTime(timezone=True))
    linked_downtime_event_id = Column(UUID(as_uuid=True), ForeignKey("downtime_events.id"), nullable=True)
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    completed_at = Column(DateTime(timezone=True))
    completed_by = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=True)
    labor_hours = Column(Float)
    maintenance_notes = Column(String)
    resolution_summary = Column(String)

    # Relationships
    machine = relationship("Machine")
    assigned_user = relationship("User", foreign_keys=[assigned_to])

class PreventiveMaintenanceSchedule(Base):
    __tablename__ = "preventive_maintenance_schedules"

    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    description = Column(String)
    machine_id = Column(UUID(as_uuid=True), ForeignKey("machines.id"), nullable=False, index=True)
    interval_days = Column(Integer)
    runtime_threshold_hours = Column(Float)
    next_due_at = Column(DateTime(timezone=True))
    is_active = Column(Boolean, default=True)

    # Relationships
    machine = relationship("Machine")
