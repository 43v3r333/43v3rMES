from sqlalchemy import Column, String, JSON, DateTime, ForeignKey, UUID, Enum as SQLEnum
import uuid
from datetime import datetime, timezone
from enum import Enum
from backend.app.db.base_class import Base

class ReportStatus(str, Enum):
    PENDING = "PENDING"
    PROCESSING = "PROCESSING"
    COMPLETED = "COMPLETED"
    FAILED = "FAILED"

class ExportFormat(str, Enum):
    CSV = "CSV"
    XLSX = "XLSX"
    PDF = "PDF"

class ReportTemplate(Base):
    __tablename__ = "report_templates"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    name = Column(String, nullable=False)
    report_type = Column(String, nullable=False) # SHIFT_SUMMARY, MAINTENANCE, etc.
    filters_json = Column(JSON) # Saved filter configuration
    created_by = Column(UUID(as_uuid=True), ForeignKey("users.id"))

class ReportRequest(Base):
    __tablename__ = "report_requests"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    user_id = Column(UUID(as_uuid=True), ForeignKey("users.id"), nullable=False)

    report_type = Column(String, nullable=False)
    format = Column(SQLEnum(ExportFormat), nullable=False)
    status = Column(SQLEnum(ReportStatus), default=ReportStatus.PENDING, nullable=False)

    parameters = Column(JSON) # Request-specific parameters (dates, IDs)
    file_path = Column(String)
    error_message = Column(String)

    started_at = Column(DateTime(timezone=True))
    completed_at = Column(DateTime(timezone=True))

class ExportHistory(Base):
    __tablename__ = "export_history"
    id = Column(UUID(as_uuid=True), primary_key=True, default=uuid.uuid4)
    tenant_id = Column(UUID(as_uuid=True), ForeignKey("tenants.id"), nullable=False, index=True)
    report_request_id = Column(UUID(as_uuid=True), ForeignKey("report_requests.id"), nullable=False)

    filename = Column(String, nullable=False)
    file_size_bytes = Column(JSON) # Can store metadata
    download_count = Column(JSON, default=0)
