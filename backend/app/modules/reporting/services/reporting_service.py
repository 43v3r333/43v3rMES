from datetime import datetime, timezone
from typing import List, Any, Optional, Dict
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.modules.reporting.models.reporting import ReportRequest, ReportStatus, ExportFormat
from backend.app.modules.reporting.schemas.reporting import ReportRequestCreate
from backend.app.models.tenant import User

class ReportingService:
    async def initiate_report(self, db: AsyncSession, obj_in: ReportRequestCreate, user: User) -> ReportRequest:
        db_obj = ReportRequest(
            tenant_id=user.tenant_id,
            user_id=user.id,
            report_type=obj_in.report_type,
            format=obj_in.format,
            parameters=obj_in.parameters,
            status=ReportStatus.PENDING,
            started_at=datetime.now(timezone.utc)
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)

        # Trigger background task here
        # run_report_generation.delay(db_obj.id)

        return db_obj

    async def get_report_status(self, db: AsyncSession, request_id: UUID, tenant_id: UUID) -> Optional[ReportRequest]:
        from sqlalchemy import select
        result = await db.execute(
            select(ReportRequest).where(ReportRequest.id == request_id, ReportRequest.tenant_id == tenant_id)
        )
        return result.scalars().first()

reporting_service = ReportingService()
