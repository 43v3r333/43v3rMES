from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime, timedelta, timezone
from backend.app.api import deps
from backend.app.modules.analytics.services.analytics_service import analytics_service
from backend.app.modules.analytics.schemas.analytics import KPIResponse, ParetoItem, TrendResponse, AgingIssue
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/kpis", response_model=KPIResponse)
async def get_kpis(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    start_date: Optional[datetime] = None,
    end_date: Optional[datetime] = None,
) -> Any:
    if not end_date:
        end_date = datetime.now(timezone.utc)
    if not start_date:
        start_date = end_date - timedelta(days=30)

    return await analytics_service.get_kpis(db, current_user.tenant_id, start_date, end_date)

@router.get("/pareto", response_model=List[ParetoItem])
async def get_pareto(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
    group_by: str = Query("category", regex="^(category|machine|line|shift)$")
) -> Any:
    return await analytics_service.get_pareto_by_category(db, current_user.tenant_id)

@router.get("/open-issues", response_model=List[AgingIssue])
async def get_open_issues(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Logic to fetch open issues with aging calculation
    return []
