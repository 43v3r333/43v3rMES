from typing import Optional, Any, List
from pydantic import BaseModel
import uuid
from datetime import datetime

class NotificationBase(BaseModel):
    title: str
    message: str
    type: Optional[str] = "SYSTEM"
    severity: Optional[str] = "INFO"
    link_to_entity_type: Optional[str] = None
    link_to_entity_id: Optional[uuid.UUID] = None

class NotificationCreate(NotificationBase):
    user_id: uuid.UUID

class Notification(NotificationBase):
    id: uuid.UUID
    user_id: uuid.UUID
    is_read: bool
    is_acknowledged: bool
    created_at: datetime
    class Config: from_attributes = True

class EscalationRuleBase(BaseModel):
    name: str
    entity_type: str
    condition_type: str
    threshold_value: int
    escalate_to_role: Optional[str] = None
    new_severity: Optional[str] = None
    is_active: bool = True

class EscalationRuleCreate(EscalationRuleBase):
    pass

class EscalationRule(EscalationRuleBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class AlertEvent(BaseModel):
    id: uuid.UUID
    event_type: str
    severity: str
    message: str
    source_entity_type: Optional[str] = None
    source_entity_id: Optional[uuid.UUID] = None
    created_at: datetime
    class Config: from_attributes = True
