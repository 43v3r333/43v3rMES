from typing import List, Dict, Any, Optional
from pydantic import BaseModel
from datetime import datetime

class KPIResponse(BaseModel):
    mttr: float
    mtbf: float
    availability: float
    downtime_percentage: float
    open_issue_count: int
    escalation_count: int

class ParetoItem(BaseModel):
    label: str
    value: float
    percentage: float
    cumulative_percentage: float

class TrendDataPoint(BaseModel):
    timestamp: datetime
    value: float

class TrendResponse(BaseModel):
    metric: str
    data_points: List[TrendDataPoint]

class AgingIssue(BaseModel):
    event_number: str
    title: str
    age_hours: float
    status: str
    severity: str
