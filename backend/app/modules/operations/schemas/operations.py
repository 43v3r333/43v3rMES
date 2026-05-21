from typing import List, Optional, Any
from pydantic import BaseModel
import uuid
from datetime import datetime

class MachineStatus(BaseModel):
    machine_id: uuid.UUID
    name: str
    code: str
    status: str # RUNNING, IDLE, DOWN
    active_event_id: Optional[uuid.UUID] = None

class ActiveIncident(BaseModel):
    id: uuid.UUID
    event_number: str
    title: str
    severity: str
    started_at: datetime
    duration_minutes: int
    machines: List[str]

class OperationsOverview(BaseModel):
    active_incident_count: int
    critical_alert_count: int
    mttr_last_24h: float
    availability_score: float
    current_shift_name: str
    supervisor_on_duty: str

class AlertStreamItem(BaseModel):
    id: uuid.UUID
    timestamp: datetime
    severity: str
    message: str
    source: str
