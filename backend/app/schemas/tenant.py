from typing import Optional
from pydantic import BaseModel
import uuid

class TenantBase(BaseModel):
    name: str
    slug: str
    is_active: Optional[bool] = True

class TenantCreate(TenantBase):
    pass

class TenantUpdate(BaseModel):
    name: Optional[str] = None
    slug: Optional[str] = None
    is_active: Optional[bool] = None

class Tenant(TenantBase):
    id: uuid.UUID
    class Config: from_attributes = True
