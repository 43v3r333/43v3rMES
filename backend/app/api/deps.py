from typing import Generator, Optional
from fastapi import Depends, HTTPException, status
from fastapi.security import OAuth2PasswordBearer
from jose import jwt, JWTError
from pydantic import ValidationError
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.tenant import User
from backend.app.schemas.user import TokenPayload
from sqlalchemy import select
from sqlalchemy.orm import selectinload
import uuid

reusable_oauth2 = OAuth2PasswordBearer(
    tokenUrl=f"{settings.API_V1_STR}/auth/login"
)

async def get_current_user(
    db: AsyncSession = Depends(get_db),
    token: str = Depends(reusable_oauth2)
) -> User:
    try:
        payload = jwt.decode(
            token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
        )
        token_data = TokenPayload(**payload)
    except (JWTError, ValidationError):
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Could not validate credentials",
        )

    result = await db.execute(
        select(User)
        .options(
            selectinload(User.roles),
            selectinload(User.refresh_tokens)
        )
        .where(User.id == uuid.UUID(token_data.sub))
    )
    user = result.scalars().first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return user

async def get_current_active_user(
    current_user: User = Depends(get_current_user),
) -> User:
    if not current_user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")
    return current_user

async def get_current_tenant_id(
    current_user: User = Depends(get_current_active_user),
) -> uuid.UUID:
    if not current_user.tenant_id:
        raise HTTPException(status_code=400, detail="User not assigned to a tenant")
    return current_user.tenant_id

# Tenant Isolation Helper
async def get_db_with_tenant(
    db: AsyncSession = Depends(get_db),
    tenant_id: uuid.UUID = Depends(get_current_tenant_id)
) -> AsyncSession:
    # In a real enterprise app, we might set a search_path or use a scoped query
    # For now, this dependency ensures tenant_id is available for filtering in repositories
    return db
