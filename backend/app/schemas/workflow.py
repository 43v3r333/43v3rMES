from typing import Optional, List, Any
from pydantic import BaseModel
import uuid
from datetime import datetime, time

class ShiftBase(BaseModel):
    name: str
    start_time: time
    end_time: time
    factory_id: uuid.UUID
    is_active: bool = True

class ShiftCreate(ShiftBase):
    pass

class Shift(ShiftBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class ShiftHandoverBase(BaseModel):
    outgoing_shift_id: uuid.UUID
    incoming_shift_id: uuid.UUID
    supervisor_id: uuid.UUID
    date: datetime
    operational_concerns: Optional[str] = None
    maintenance_notes: Optional[str] = None
    production_risks: Optional[str] = None
    escalation_tracking: Optional[str] = None

class ShiftHandoverCreate(ShiftHandoverBase):
    carryover_event_ids: List[uuid.UUID] = []

class ShiftHandover(ShiftHandoverBase):
    id: uuid.UUID
    tenant_id: uuid.UUID
    class Config: from_attributes = True

class ShiftNoteBase(BaseModel):
    content: str
    category: Optional[str] = "Operational"

class ShiftNoteCreate(ShiftNoteBase):
    handover_id: Optional[uuid.UUID] = None

class ShiftNote(ShiftNoteBase):
    id: uuid.UUID
    user_id: uuid.UUID
    created_at: datetime
    class Config: from_attributes = True

class AuditEventBase(BaseModel):
    entity_type: str
    entity_id: uuid.UUID
    action_type: str
    change_reason: Optional[str] = None

class AuditEvent(AuditEventBase):
    id: uuid.UUID
    user_id: uuid.UUID
    timestamp: datetime
    previous_state: Optional[Any] = None
    new_state: Optional[Any] = None
    class Config: from_attributes = True
