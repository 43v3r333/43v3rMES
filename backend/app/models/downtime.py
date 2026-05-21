from sqlalchemy import Column, String, Integer, DateTime, ForeignKey, UUID, Table, Enum as SQLEnum
from sqlalchemy.orm import relationship
import uuid
from enum import Enum
from backend.app.db.base_class import Base

class DowntimeStatus(str, Enum):
    OPEN = "OPEN"
    IN_PROGRESS = "IN_PROGRESS"
    RESOLVED = "RESOLVED"
    CLOSED = "CLOSED"

class DowntimeSeverity(str, Enum):
    LOW = "LOW"
    MEDIUM = "MEDIUM"
    HIGH = "HIGH"
    CRITICAL = "CRITICAL"

# Association table for DowntimeEvent - Machine
downtime_event_machines = Table(
    "downtime_event_machines",
    Base.metadata,
    Column("event_id", UUID(as_uuid=True), ForeignKey("downtime_events.id"), primary_key=True),
    Column("machine_id", UUID(as_uuid=True), ForeignKey("machines.id"), primary_key=True),
)

class DowntimeCategory(Base):
    __tablename__ = "downtime_categories"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    name = Column(String, nullable=False)
    description = Column(String)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

class DowntimeEvent(Base):
    __tablename__ = "downtime_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    factory_id = Column(UUID(as_uuid=True), ForeignKey("factories.id"), nullable=False)
    area_id = Column(UUID(as_uuid=True), ForeignKey("areas.id"), nullable=False)
    production_line_id = Column(UUID(as_uuid=True), ForeignKey("production_lines.id"), nullable=False)

    event_number = Column(String, unique=True, index=True)
    title = Column(String, nullable=False)
    description = Column(String)
    root_cause = Column(String)
    resolution_notes = Column(String)

    status = Column(SQLEnum(DowntimeStatus), default=DowntimeStatus.OPEN, nullable=False, index=True)
    severity = Column(SQLEnum(DowntimeSeverity), default=DowntimeSeverity.MEDIUM, nullable=False, index=True)
    category_id = Column(UUID(as_uuid=True), ForeignKey("downtime_categories.id"))

    started_at = Column(DateTime(timezone=True), nullable=False)
    ended_at = Column(DateTime(timezone=True))
    duration_minutes = Column(Integer)

    reported_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    created_by = Column(UUID(as_uuid=True))
    updated_by = Column(UUID(as_uuid=True))

    # Relationships
    machines = relationship("Machine", secondary=downtime_event_machines)
    category = relationship("DowntimeCategory")
    comments = relationship("DowntimeComment", back_populates="event", cascade="all, delete-orphan")
    attachments = relationship("DowntimeAttachment", back_populates="event", cascade="all, delete-orphan")

class DowntimeComment(Base):
    __tablename__ = "downtime_comments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("downtime_events.id"), nullable=False)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)
    content = Column(String, nullable=False)

    event = relationship("DowntimeEvent", back_populates="comments")
    user = relationship("User")

class DowntimeAttachment(Base):
    __tablename__ = "downtime_attachments"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    event_id = Column(UUID(as_uuid=True), ForeignKey("downtime_events.id"), nullable=False)
    file_name = Column(String, nullable=False)
    file_path = Column(String, nullable=False)
    file_type = Column(String)
    uploaded_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

    event = relationship("DowntimeEvent", back_populates="attachments")
