from typing import List, Optional
from uuid import UUID
from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.base import BaseRepository
from backend.app.models.factory import Factory, Area, ProductionLine, Machine
from backend.app.schemas.factory import (
    FactoryCreate, FactoryUpdate,
    AreaCreate, AreaUpdate,
    ProductionLineCreate, ProductionLineUpdate,
    MachineCreate, MachineUpdate
)

class FactoryRepository(BaseRepository[Factory, FactoryCreate, FactoryUpdate]):
    async def get_by_tenant(self, db: AsyncSession, tenant_id: UUID, skip: int = 0, limit: int = 100) -> List[Factory]:
        result = await db.execute(
            select(Factory).where(Factory.tenant_id == tenant_id, Factory.is_deleted == False).offset(skip).limit(limit)
        )
        return result.scalars().all()

class AreaRepository(BaseRepository[Area, AreaCreate, AreaUpdate]):
    async def get_by_factory(self, db: AsyncSession, factory_id: UUID, tenant_id: UUID) -> List[Area]:
        result = await db.execute(
            select(Area).where(Area.factory_id == factory_id, Area.tenant_id == tenant_id, Area.is_deleted == False)
        )
        return result.scalars().all()

class ProductionLineRepository(BaseRepository[ProductionLine, ProductionLineCreate, ProductionLineUpdate]):
    async def get_by_area(self, db: AsyncSession, area_id: UUID, tenant_id: UUID) -> List[ProductionLine]:
        result = await db.execute(
            select(ProductionLine).where(ProductionLine.area_id == area_id, ProductionLine.tenant_id == tenant_id, ProductionLine.is_deleted == False)
        )
        return result.scalars().all()

class MachineRepository(BaseRepository[Machine, MachineCreate, MachineUpdate]):
    async def get_by_line(self, db: AsyncSession, line_id: UUID, tenant_id: UUID) -> List[Machine]:
        result = await db.execute(
            select(Machine).where(Machine.line_id == line_id, Machine.tenant_id == tenant_id, Machine.is_deleted == False)
        )
        return result.scalars().all()

factory_repo = FactoryRepository(Factory)
area_repo = AreaRepository(Area)
line_repo = ProductionLineRepository(ProductionLine)
machine_repo = MachineRepository(Machine)
