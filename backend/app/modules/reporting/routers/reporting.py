from typing import Any, List, Optional
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.reporting.services.reporting_service import reporting_service
from backend.app.modules.reporting.repositories.report_repo import report_repo, request_repo
from backend.app.modules.reporting.schemas.reporting import ReportRequest, ReportRequestCreate, ReportTemplate
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/templates", response_model=List[ReportTemplate])
async def read_report_templates(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await report_repo.get_by_tenant(db, current_user.tenant_id)

@router.post("/generate", response_model=ReportRequest)
async def create_report_request(
    *,
    db: AsyncSession = Depends(deps.get_db),
    request_in: ReportRequestCreate,
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await reporting_service.initiate_report(db, request_in, current_user)

@router.get("/export-history", response_model=List[ReportRequest])
async def read_export_history(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return await request_repo.get_history_by_tenant(db, current_user.tenant_id)

@router.get("/{request_id}", response_model=ReportRequest)
async def read_report_status(
    request_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    status = await reporting_service.get_report_status(db, request_id, current_user.tenant_id)
    if not status:
        raise HTTPException(status_code=404, detail="Report request not found")
    return status
