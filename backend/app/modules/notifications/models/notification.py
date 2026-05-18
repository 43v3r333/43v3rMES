from sqlalchemy import Column, String, Boolean, DateTime, ForeignKey, UUID, Integer, JSON
from sqlalchemy.orm import relationship
import uuid
from datetime import datetime, timezone
from backend.app.db.base_class import Base

class Notification(Base):
    __tablename__ = "notifications"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    message = Column(String, nullable=False)
    type = Column(String) # e.g., ASSIGNMENT, ESCALATION, SYSTEM
    severity = Column(String, default="INFO")

    is_read = Column(Boolean, default=False)
    is_acknowledged = Column(Boolean, default=False)
    acknowledged_at = Column(DateTime(timezone=True))

    link_to_entity_type = Column(String) # e.g., DowntimeEvent
    link_to_entity_id = Column(UUID(as_uuid=True))

    user = relationship("User")

class EscalationRule(Base):
    __tablename__ = "escalation_rules"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    name = Column(String, nullable=False)
    entity_type = Column(String, nullable=False) # e.g., DowntimeEvent
    condition_type = Column(String, nullable=False) # e.g., DURATION_EXCEEDS, CRITICAL_DETECTED
    threshold_value = Column(Integer) # e.g., minutes

    escalate_to_role = Column(String)
    new_severity = Column(String)
    is_active = Column(Boolean, default=True)

class AssignmentHistory(Base):
    __tablename__ = "assignment_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    entity_type = Column(String, nullable=False)
    entity_id = Column(UUID(as_uuid=True), nullable=False)

    assigned_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_to = Column(UUID(as_uuid=True), ForeignKey("users.id"))
    assigned_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class AlertEvent(Base):
    __tablename__ = "alert_events"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    event_type = Column(String, nullable=False)
    severity = Column(String, nullable=False)
    message = Column(String, nullable=False)
    source_entity_type = Column(String)
    source_entity_id = Column(UUID(as_uuid=True))
    metadata_json = Column(JSON)
