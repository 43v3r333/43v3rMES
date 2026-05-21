from typing import List, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.factory import factory_repo, area_repo, line_repo, machine_repo
from backend.app.schemas.factory import FactoryCreate, AreaCreate, ProductionLineCreate, MachineCreate
from backend.app.models.tenant import User

class FactoryService:
    async def create_factory(self, db: AsyncSession, obj_in: FactoryCreate, user: User) -> Any:
        # Repository expects schema that includes tenant_id
        data = obj_in.model_dump()
        data["tenant_id"] = user.tenant_id
        data["created_by"] = user.id
        # We need a schema that includes tenant_id for the repo's generic create
        # or we just use the model directly here if repo is too strict.
        # Let's adjust repo or use a temporary schema.
        from backend.app.models.factory import Factory
        db_obj = Factory(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def get_factories(self, db: AsyncSession, user: User) -> List[Any]:
        return await factory_repo.get_by_tenant(db, user.tenant_id)

    async def create_area(self, db: AsyncSession, obj_in: AreaCreate, user: User) -> Any:
        data = obj_in.model_dump()
        data["tenant_id"] = user.tenant_id
        data["created_by"] = user.id
        from backend.app.models.factory import Area
        db_obj = Area(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def create_machine(self, db: AsyncSession, obj_in: MachineCreate, user: User) -> Any:
        data = obj_in.model_dump()
        data["tenant_id"] = user.tenant_id
        data["created_by"] = user.id
        from backend.app.models.factory import Machine
        db_obj = Machine(**data)
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

factory_service = FactoryService()
