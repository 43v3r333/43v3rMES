from typing import Any, List, Optional
from fastapi import APIRouter, Depends, Query
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.enterprise.services.enterprise_service import enterprise_service
from backend.app.modules.enterprise.schemas.enterprise import EnterpriseOverview, SiteComparisonItem
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/overview", response_model=EnterpriseOverview)
async def get_enterprise_overview(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await enterprise_service.get_enterprise_overview(db, current_user.tenant_id)

@router.get("/site-comparison", response_model=List[SiteComparisonItem])
async def get_site_comparisons(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await enterprise_service.get_site_comparisons(db, current_user.tenant_id)

@router.get("/organizations")
async def get_organizations(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Logic to fetch organizations for the tenant
    return []
