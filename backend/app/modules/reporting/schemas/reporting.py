from typing import Optional, Any, List, Dict
from pydantic import BaseModel
import uuid
from datetime import datetime
from backend.app.modules.reporting.models.reporting import ReportStatus, ExportFormat

class ReportTemplateBase(BaseModel):
    name: str
    report_type: str
    filters_json: Optional[Dict[str, Any]] = None

class ReportTemplateCreate(ReportTemplateBase):
    pass

class ReportTemplate(ReportTemplateBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    class Config: from_attributes = True

class ReportRequestCreate(BaseModel):
    report_type: str
    format: ExportFormat
    parameters: Optional[Dict[str, Any]] = None

class ReportRequest(BaseModel):
    id: uuid.UUID
    report_type: str
    format: ExportFormat
    status: ReportStatus
    parameters: Optional[Dict[str, Any]] = None
    started_at: Optional[datetime] = None
    completed_at: Optional[datetime] = None
    file_path: Optional[str] = None

    class Config: from_attributes = True

class ExportHistory(BaseModel):
    id: uuid.UUID
    filename: str
    report_request_id: uuid.UUID
    created_at: datetime

    class Config: from_attributes = True
