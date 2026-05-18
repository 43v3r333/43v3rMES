from typing import Optional
from pydantic import BaseModel, EmailStr
import uuid
class UserBase(BaseModel):
    email: Optional[EmailStr] = None
    is_active: Optional[bool] = True
    is_superuser: bool = False
    full_name: Optional[str] = None
    tenant_id: Optional[uuid.UUID] = None
class UserCreate(UserBase):
    email: EmailStr
    password: str
class UserInDBBase(UserBase):
    id: Optional[uuid.UUID] = None
    class Config: from_attributes = True
class User(UserInDBBase): pass
class Token(BaseModel):
    access_token: str
    token_type: str
