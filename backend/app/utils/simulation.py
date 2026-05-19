import random
from datetime import datetime, timedelta, timezone
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.models.downtime import DowntimeEvent, DowntimeStatus, DowntimeSeverity
from sqlalchemy import select

class OperationalSimulator:
    async def simulate_downtime_wave(self, db: AsyncSession, tenant_id: UUID, factory_id: UUID, count: int = 10):
        """
        Generates a wave of downtime events across random machines to test escalation and analytics.
        """
        # 1. Fetch some machines
        from backend.app.models.factory import Machine
        m_result = await db.execute(select(Machine).where(Machine.tenant_id == tenant_id).limit(20))
        machines = m_result.scalars().all()

        if not machines:
            return

        for _ in range(count):
            target_machine = random.choice(machines)
            event = DowntimeEvent(
                tenant_id=tenant_id,
                factory_id=factory_id,
                area_id=UUID("00000000-0000-0000-0000-000000000001"), # Mock
                production_line_id=target_machine.line_id,
                event_number=f"SIM-{random.randint(1000, 9999)}",
                title=random.choice(["Sensor Failure", "Belt Slip", "Motor Overheat", "Material Jam"]),
                status=DowntimeStatus.OPEN,
                severity=random.choice(list(DowntimeSeverity)),
                started_at=datetime.now(timezone.utc) - timedelta(minutes=random.randint(10, 240))
            )
            event.machines.append(target_machine)
            db.add(event)

        await db.commit()

simulator = OperationalSimulator()
