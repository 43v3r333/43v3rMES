from sqlalchemy import Column, String, DateTime, ForeignKey, UUID, JSON, Table, Time, Boolean
from sqlalchemy.orm import relationship
import uuid
from backend.app.db.base_class import Base

# Association for Handovers to Carryover DowntimeEvents
handover_carryover_events = Table(
    "handover_carryover_events",
    Base.metadata,
    Column("handover_id", UUID(as_uuid=True), ForeignKey("shift_handovers.id"), primary_key=True),
    Column("event_id", UUID(as_uuid=True), ForeignKey("downtime_events.id"), primary_key=True),
)

class Shift(Base):
    __tablename__ = "shifts"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False) # e.g., Day Shift, Night Shift
    start_time = Column(Time, nullable=False)
    end_time = Column(Time, nullable=False)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    factory_id = Column(UUID(as_uuid=True), ForeignKey("factories.id"), nullable=False)
    is_active = Column(Boolean, default=True)

class ShiftAssignment(Base):
    __tablename__ = "shift_assignments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)
    role_description = Column(String)

    shift = relationship("Shift")
    user = relationship("User")

class ShiftHandover(Base):
    __tablename__ = "shift_handovers"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    outgoing_shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    incoming_shift_id = Column(UUID(as_uuid=True), ForeignKey("shifts.id"), nullable=False)
    supervisor_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    date = Column(DateTime(timezone=True), nullable=False)

    operational_concerns = Column(String)
    maintenance_notes = Column(String)
    production_risks = Column(String)
    escalation_tracking = Column(String)

    carryover_events = relationship("DowntimeEvent", secondary=handover_carryover_events)
    notes = relationship("ShiftNote", back_populates="handover")

class ShiftNote(Base):
    __tablename__ = "shift_notes"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    handover_id = Column(UUID(as_uuid=True), ForeignKey("shift_handovers.id"))
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)
    category = Column(String) # Operational, Safety, Quality

    handover = relationship("ShiftHandover", back_populates="notes")
    user = relationship("User")

class AuditEvent(Base):
    __tablename__ = "audit_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    entity_type = Column(String, nullable=False, index=True) # e.g., DowntimeEvent, ShiftHandover
    entity_id = Column(UUID(as_uuid=True), nullable=False, index=True)
    action_type = Column(String, nullable=False) # CREATE, UPDATE, DELETE, ESCALATE
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    timestamp = Column(DateTime(timezone=True), nullable=False)

    previous_state = Column(JSON)
    new_state = Column(JSON)
    change_reason = Column(String)

    user = relationship("User")
