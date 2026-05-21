from typing import Optional, List, Any, Dict
from pydantic import BaseModel
import uuid
from datetime import datetime

class AIShiftSummary(BaseModel):
    id: uuid.UUID
    shift_name: str
    date: datetime
    summary_text: str
    top_issues: List[str]
    maintenance_highlights: List[str]
    risk_level: str # LOW, MEDIUM, HIGH
    confidence: float

class RecurringIssue(BaseModel):
    id: uuid.UUID
    machine_id: uuid.UUID
    issue_signature: str
    description: str
    occurrence_count: int
    last_occurrence: datetime

    class Config: from_attributes = True

class RiskAnalysis(BaseModel):
    entity_id: uuid.UUID
    entity_name: str
    risk_score: float # 0-100
    risk_factors: List[str]
    suggested_actions: List[str]

class OperationalRecommendation(BaseModel):
    id: uuid.UUID
    title: str
    description: str
    severity: str
    action_item: Optional[str] = None
    created_at: datetime

    class Config: from_attributes = True

class RecommendationUpdate(BaseModel):
    status: str # IMPLEMENTED, DISMISSED
