from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, UUID, Float, Boolean
import uuid
from datetime import datetime, timezone
from backend.app.db.base_class import Base

class AIInsight(Base):
    __tablename__ = "ai_insights"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    insight_type = Column(String, nullable=False, index=True) # SHIFT_SUMMARY, RISK_ANALYSIS, RECURRING_ISSUE
    entity_type = Column(String) # Machine, Factory, ProductionLine
    entity_id = Column(UUID(as_uuid=True))

    content_json = Column(JSON, nullable=False) # The generated analysis
    confidence_score = Column(Float, default=1.0)

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class OperationalRecommendation(Base):
    __tablename__ = "operational_recommendations"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    title = Column(String, nullable=False)
    description = Column(String, nullable=False)
    severity = Column(String, default="MEDIUM") # INFO, MEDIUM, HIGH, CRITICAL
    status = Column(String, default="OPEN") # OPEN, IMPLEMENTED, DISMISSED

    action_item = Column(String)
    source_insight_id = Column(UUID(as_uuid=True), ForeignKey("ai_insights.id"))

    created_at = Column(DateTime(timezone=True), default=lambda: datetime.now(timezone.utc))

class RecurringIssue(Base):
    __tablename__ = "recurring_issues"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)

    issue_signature = Column(String, nullable=False, index=True) # Hash or code identifying the issue pattern
    description = Column(String, nullable=False)
    occurrence_count = Column(Float, default=1)
    last_occurrence_at = Column(DateTime(timezone=True))

    machine_id = Column(UUID(as_uuid=True), ForeignKey("machines.id"))
