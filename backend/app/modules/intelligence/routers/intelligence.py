from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.intelligence.services.intelligence_service import intelligence_service
from backend.app.modules.intelligence.analyzers.risk_analyzer import risk_analyzer
from backend.app.modules.intelligence.schemas.intelligence import AIShiftSummary, RiskAnalysis, OperationalRecommendation, RecurringIssue
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/shift-summaries", response_model=AIShiftSummary)
async def get_shift_summary(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await intelligence_service.get_shift_summary(db, current_user.tenant_id)

@router.get("/recommendations", response_model=List[OperationalRecommendation])
async def get_recommendations(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await intelligence_service.get_recommendations(db, current_user.tenant_id)

@router.get("/risk-analysis/{machine_id}", response_model=RiskAnalysis)
async def get_risk_analysis(
    machine_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await risk_analyzer.analyze_machine_risk(db, machine_id)
