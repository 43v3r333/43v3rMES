from typing import Optional, List
from pydantic import BaseModel
import uuid
from datetime import datetime

class BaseHierarchy(BaseModel):
    name: str
    description: Optional[str] = None

class BaseHierarchyInDB(BaseHierarchy):
    id: uuid.UUID
    tenant_id: uuid.UUID
    created_at: datetime
    updated_at: datetime
    created_by: Optional[uuid.UUID] = None
    updated_by: Optional[uuid.UUID] = None

    class Config:
        from_attributes = True

# Machine
class MachineCreate(BaseHierarchy):
    code: str
    line_id: uuid.UUID

class MachineUpdate(BaseHierarchy):
    name: Optional[str] = None
    code: Optional[str] = None
    line_id: Optional[uuid.UUID] = None

class Machine(BaseHierarchyInDB):
    code: str
    line_id: uuid.UUID

# Production Line
class ProductionLineCreate(BaseHierarchy):
    area_id: uuid.UUID

class ProductionLineUpdate(BaseHierarchy):
    name: Optional[str] = None
    area_id: Optional[uuid.UUID] = None

class ProductionLine(BaseHierarchyInDB):
    area_id: uuid.UUID
    machines: List[Machine] = []

# Area
class AreaCreate(BaseHierarchy):
    factory_id: uuid.UUID

class AreaUpdate(BaseHierarchy):
    name: Optional[str] = None
    factory_id: Optional[uuid.UUID] = None

class Area(BaseHierarchyInDB):
    factory_id: uuid.UUID
    production_lines: List[ProductionLine] = []

# Factory
class FactoryCreate(BaseHierarchy):
    pass

class FactoryUpdate(BaseHierarchy):
    name: Optional[str] = None

class Factory(BaseHierarchyInDB):
    areas: List[Area] = []
