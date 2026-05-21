from typing import List, Any
from uuid import UUID
from datetime import datetime, timezone, timedelta
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, func
from backend.app.models.downtime import DowntimeEvent, DowntimeStatus
from backend.app.models.factory import Machine
from backend.app.modules.operations.schemas.operations import OperationsOverview, ActiveIncident, MachineStatus

class OperationsService:
    async def get_overview(self, db: AsyncSession, tenant_id: UUID) -> OperationsOverview:
        # Optimized counts
        incident_count = await db.execute(
            select(func.count(DowntimeEvent.id)).where(
                DowntimeEvent.tenant_id == tenant_id,
                DowntimeEvent.status != DowntimeStatus.RESOLVED,
                DowntimeEvent.is_deleted == False
            )
        )

        return OperationsOverview(
            active_incident_count=incident_count.scalar() or 0,
            critical_alert_count=0, # Placeholder
            mttr_last_24h=42.5, # Placeholder
            availability_score=98.4, # Placeholder
            current_shift_name="Day Shift",
            supervisor_on_duty="John Doe"
        )

    async def get_active_incidents(self, db: AsyncSession, tenant_id: UUID) -> List[ActiveIncident]:
        from sqlalchemy.orm import selectinload
        result = await db.execute(
            select(DowntimeEvent)
            .options(selectinload(DowntimeEvent.machines))
            .where(
                DowntimeEvent.tenant_id == tenant_id,
                DowntimeEvent.status != DowntimeStatus.RESOLVED,
                DowntimeEvent.is_deleted == False
            )
            .order_by(DowntimeEvent.started_at.desc())
        )
        events = result.scalars().all()

        return [
            ActiveIncident(
                id=e.id,
                event_number=e.event_number,
                title=e.title,
                severity=e.severity.value,
                started_at=e.started_at,
                duration_minutes=int((datetime.now(timezone.utc) - e.started_at).total_seconds() / 60),
                machines=[m.code for m in e.machines]
            ) for e in events
        ]

operations_service = OperationsService()
