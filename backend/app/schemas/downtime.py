from typing import Optional, List
from pydantic import BaseModel
import uuid
from datetime import datetime
from backend.app.models.downtime import DowntimeStatus, DowntimeSeverity

class DowntimeCategoryBase(BaseModel):
    name: str
    description: Optional[str] = None

class DowntimeCategoryCreate(DowntimeCategoryBase):
    pass

class DowntimeCategory(DowntimeCategoryBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class DowntimeCommentBase(BaseModel):
    content: str

class DowntimeCommentCreate(DowntimeCommentBase):
    event_id: uuid.UUID

class DowntimeComment(DowntimeCommentBase):
    id: uuid.UUID
    event_id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    class Config: from_attributes = True

class DowntimeAttachmentBase(BaseModel):
    file_name: str
    file_type: Optional[str] = None

class DowntimeAttachment(DowntimeAttachmentBase):
    id: uuid.UUID
    file_path: str
    uploaded_by: uuid.UUID
    class Config: from_attributes = True

class DowntimeEventBase(BaseModel):
    title: str
    description: Optional[str] = None
    factory_id: uuid.UUID
    area_id: uuid.UUID
    production_line_id: uuid.UUID
    status: DowntimeStatus = DowntimeStatus.OPEN
    severity: DowntimeSeverity = DowntimeSeverity.MEDIUM
    category_id: Optional[uuid.UUID] = None
    started_at: datetime
    ended_at: Optional[datetime] = None

class DowntimeEventCreate(DowntimeEventBase):
    machine_ids: List[uuid.UUID] = []

class DowntimeEventUpdate(BaseModel):
    title: Optional[str] = None
    description: Optional[str] = None
    root_cause: Optional[str] = None
    resolution_notes: Optional[str] = None
    status: Optional[DowntimeStatus] = None
    severity: Optional[DowntimeSeverity] = None
    category_id: Optional[uuid.UUID] = None
    ended_at: Optional[datetime] = None
    assigned_to: Optional[uuid.UUID] = None

class DowntimeEvent(DowntimeEventBase):
    id: uuid.UUID
    event_number: str
    root_cause: Optional[str] = None
    resolution_notes: Optional[str] = None
    duration_minutes: Optional[int] = None
    reported_by: Optional[uuid.UUID] = None
    assigned_to: Optional[uuid.UUID] = None
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime

    # Nested relationships can be added here or as separate schemas
    # machines: List[Any] = []

    class Config: from_attributes = True
