from typing import List, Any
from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.models.downtime import DowntimeEvent, DowntimeStatus
from backend.app.modules.analytics.calculators.metrics import MetricCalculator
from backend.app.modules.analytics.schemas.analytics import KPIResponse, ParetoItem

class AnalyticsService:
    async def get_kpis(self, db: AsyncSession, tenant_id: UUID, start_date: datetime, end_date: datetime) -> KPIResponse:
        # Fetch events for the period
        result = await db.execute(
            select(DowntimeEvent).where(
                DowntimeEvent.tenant_id == tenant_id,
                DowntimeEvent.started_at >= start_date,
                DowntimeEvent.started_at <= end_date,
                DowntimeEvent.is_deleted == False
            )
        )
        events = result.scalars().all()

        total_period_minutes = int((end_date - start_date).total_seconds() / 60)
        downtime_minutes = sum(e.duration_minutes or 0 for e in events)

        open_count_result = await db.execute(
            select(func.count(DowntimeEvent.id)).where(
                DowntimeEvent.tenant_id == tenant_id,
                DowntimeEvent.status != DowntimeStatus.RESOLVED,
                DowntimeEvent.is_deleted == False
            )
        )

        return KPIResponse(
            mttr=MetricCalculator.calculate_mttr(events),
            mtbf=MetricCalculator.calculate_mtbf(events, total_period_minutes),
            availability=MetricCalculator.calculate_availability(total_period_minutes, downtime_minutes),
            downtime_percentage=(downtime_minutes / total_period_minutes * 100) if total_period_minutes > 0 else 0,
            open_issue_count=open_count_result.scalar() or 0,
            escalation_count=0 # Placeholder for now
        )

    async def get_pareto_by_category(self, db: AsyncSession, tenant_id: UUID) -> List[ParetoItem]:
        # Implementation for Pareto aggregation
        # Group by category, sum duration, sort desc
        return []

analytics_service = AnalyticsService()
