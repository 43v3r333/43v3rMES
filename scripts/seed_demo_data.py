import asyncio
import uuid
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession, async_sessionmaker
from backend.app.models.tenant import Tenant, User, Role, Permission
from backend.app.models.factory import Region, Factory, Area, ProductionLine, Machine
from backend.app.models.downtime import DowntimeEvent, DowntimeStatus, DowntimeSeverity
# Updated import path for maintenance models
from backend.app.modules.maintenance.models.maintenance import WorkOrder, WorkOrderStatus, PreventiveMaintenanceSchedule
from backend.app.core.security import get_password_hash

async def seed_data():
    DATABASE_URL = "postgresql+asyncpg://user:password@localhost:5432/mes_db"
    engine = create_async_engine(DATABASE_URL)
    async_session = async_sessionmaker(engine, expire_on_commit=False)
    # Ensure all tables are created
    from backend.app.db.base_class import Base
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)
    async with async_session() as session:
        print("Seeding Enterprise Demo Data...")

        # 1. Tenant
        tenant = Tenant(id=uuid.uuid4(), name="43v3r Industrial Group", slug="43v3r-industrial")
        session.add(tenant)
        await session.flush()  # get tenant.id
        # 2. Region
        region = Region(id=uuid.uuid4(), name="North Region", tenant_id=tenant.id)
        session.add(region)
        await session.flush()
        # 3. Factory linked to region
        factory = Factory(id=uuid.uuid4(), name="43v3r Factory Alpha", tenant_id=tenant.id, region_id=region.id)
        session.add(factory)
        await session.flush()
        # 4. Area linked to factory
        area = Area(id=uuid.uuid4(), name="Production Area 1", factory_id=factory.id, tenant_id=tenant.id)
        session.add(area)
        await session.flush()
        # 5. Production Line linked to area
        line = ProductionLine(id=uuid.uuid4(), name="Line A", area_id=area.id, tenant_id=tenant.id)
        session.add(line)
        await session.flush()
        # 6. Machine linked to line
        machine = Machine(id=uuid.uuid4(), name="Machine 1", code="MCH-001", line_id=line.id, tenant_id=tenant.id)
        session.add(machine)
        await session.flush()  # Ensure tenant exists before inserting factories


        # 2. Roles & Permissions
        admin_role = Role(id=uuid.uuid4(), name="Enterprise Admin")
        plant_manager = Role(id=uuid.uuid4(), name="Plant Manager")
        operator = Role(id=uuid.uuid4(), name="Operator")
        session.add_all([admin_role, plant_manager, operator])

        # 3. Users
        admin_user = User(
            id=uuid.uuid4(), email="admin@43v3r.com",
            hashed_password=get_password_hash("password123"),
            full_name="Enterprise Admin", tenant_id=tenant.id, is_superuser=True
        )
        session.add(admin_user)

        # 4. Factories & Hierarchy
        for i in range(2):
            factory = Factory(id=uuid.uuid4(), name=f"43v3r Factory {'Alpha' if i==0 else 'Beta'}", tenant_id=tenant.id)
            session.add(factory)
            for j in range(3):
                area = Area(id=uuid.uuid4(), name=f"Production Area {j+1}", factory_id=factory.id, tenant_id=tenant.id)
                session.add(area)
                for k in range(2):
                    line = ProductionLine(id=uuid.uuid4(), name=f"Line {chr(65+k)}", area_id=area.id, tenant_id=tenant.id)
                    session.add(line)
                    for m in range(4):
                        machine = Machine(
                            id=uuid.uuid4(), name=f"Machine {m+1}",
                            code=f"MCH-{i}{j}{k}{m}", line_id=line.id, tenant_id=tenant.id
                        )
                        session.add(machine)
                        await session.flush()

                        # 5. Seed initial downtime events
                        event = DowntimeEvent(
                            id=uuid.uuid4(), tenant_id=tenant.id,
                            factory_id=factory.id, area_id=area.id,
                            production_line_id=line.id,
                            event_number=f"DT-{uuid.uuid4().hex[:6].upper()}",
                            title="Sensor Misalignment",
                            status=DowntimeStatus.RESOLVED,
                            severity=DowntimeSeverity.MEDIUM,
                            started_at=datetime.now(timezone.utc) - timedelta(hours=2),
                            duration_minutes=45
                        )
                        session.add(event)

        await session.commit()
        print("Demo data seeding complete.")

if __name__ == "__main__":
    asyncio.run(seed_data())
