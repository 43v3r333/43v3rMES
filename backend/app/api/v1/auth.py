from datetime import datetime, timedelta, timezone
from typing import Any
from fastapi import APIRouter, Depends, HTTPException, status, Body
from fastapi.security import OAuth2PasswordRequestForm
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from backend.app.core import security
from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.tenant import User, RefreshToken, Tenant
from backend.app.schemas.user import Token, UserCreate, User as UserSchema
from backend.app.api import deps
import uuid

router = APIRouter()

@router.post("/register", response_model=UserSchema)
async def register_user(
    db: AsyncSession = Depends(get_db),
    user_in: UserCreate = Body(...)
) -> Any:
    # Check if user exists
    result = await db.execute(select(User).where(User.email == user_in.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="User with this email already exists")

    # If tenant_id provided, verify it
    if user_in.tenant_id:
        tenant_result = await db.execute(select(Tenant).where(Tenant.id == user_in.tenant_id))
        if not tenant_result.scalars().first():
            raise HTTPException(status_code=404, detail="Tenant not found")

    db_user = User(
        email=user_in.email,
        hashed_password=security.get_password_hash(user_in.password),
        full_name=user_in.full_name,
        tenant_id=user_in.tenant_id,
        is_superuser=user_in.is_superuser
    )
    db.add(db_user)
    await db.commit()
    await db.refresh(db_user)
    return db_user

@router.post("/login", response_model=Token)
async def login_access_token(
    db: AsyncSession = Depends(get_db),
    form_data: OAuth2PasswordRequestForm = Depends()
) -> Any:
    result = await db.execute(select(User).where(User.email == form_data.username))
    user = result.scalars().first()
    if not user or not security.verify_password(form_data.password, user.hashed_password):
        raise HTTPException(status_code=400, detail="Incorrect email or password")
    elif not user.is_active:
        raise HTTPException(status_code=400, detail="Inactive user")

    # Create tokens
    access_token = security.create_access_token(user.id, tenant_id=user.tenant_id)
    refresh_token_str = security.create_refresh_token()

    # Save refresh token in DB
    db_refresh = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7)
    )
    db.add(db_refresh)
    await db.commit()

    return {
        "access_token": access_token,
        "refresh_token": refresh_token_str,
        "token_type": "bearer",
    }

@router.post("/refresh", response_model=Token)
async def refresh_token(
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Body(..., embed=True)
) -> Any:
    result = await db.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc)
        )
    )
    db_token = result.scalars().first()
    if not db_token:
        raise HTTPException(status_code=401, detail="Invalid or expired refresh token")

    # Generate new access token
    access_token = security.create_access_token(db_token.user_id)

    return {
        "access_token": access_token,
        "refresh_token": refresh_token,
        "token_type": "bearer",
    }

@router.get("/me", response_model=UserSchema)
async def read_user_me(
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    return current_user

@router.post("/logout")
async def logout(
    db: AsyncSession = Depends(get_db),
    refresh_token: str = Body(..., embed=True)
) -> Any:
    result = await db.execute(select(RefreshToken).where(RefreshToken.token == refresh_token))
    db_token = result.scalars().first()
    if db_token:
        db_token.is_revoked = True
        await db.commit()
    return {"message": "Successfully logged out"}
