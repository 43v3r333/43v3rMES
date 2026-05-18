from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.base import BaseRepository
from backend.app.modules.reporting.models.reporting import ReportTemplate, ReportRequest
from backend.app.modules.reporting.schemas.reporting import ReportTemplateCreate

class ReportRepository(BaseRepository[ReportTemplate, ReportTemplateCreate, Any]):
    async def get_by_tenant(self, db: AsyncSession, tenant_id: UUID) -> List[ReportTemplate]:
        result = await db.execute(select(ReportTemplate).where(ReportTemplate.tenant_id == tenant_id, ReportTemplate.is_deleted == False))
        return result.scalars().all()

class RequestRepository(BaseRepository[ReportRequest, Any, Any]):
    async def get_history_by_tenant(self, db: AsyncSession, tenant_id: UUID) -> List[ReportRequest]:
        result = await db.execute(
            select(ReportRequest).where(ReportRequest.tenant_id == tenant_id).order_by(ReportRequest.started_at.desc())
        )
        return result.scalars().all()

report_repo = ReportRepository(ReportTemplate)
request_repo = RequestRepository(ReportRequest)
