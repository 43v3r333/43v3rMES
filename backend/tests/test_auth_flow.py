import pytest
from datetime import datetime, timedelta, timezone
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.core import security
from backend.app.core.config import settings
from backend.app.db.session import get_db
from backend.app.models.tenant import User, RefreshToken
from backend.app.schemas.user import TokenPayload
from jose import jwt
from sqlalchemy import select
import uuid


@pytest.mark.asyncio
async def test_token_refresh_flow(db_session: AsyncSession):
    user = User(
        email="test@example.com",
        hashed_password=security.get_password_hash("testpassword"),
        full_name="Test User",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    access_token = security.create_access_token(user.id, tenant_id=None)
    refresh_token_str = security.create_refresh_token()

    db_refresh = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
    )
    db_session.add(db_refresh)
    await db_session.commit()

    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    token_data = TokenPayload(**payload)
    assert token_data.sub == str(user.id)
    assert "exp" in payload

    result = await db_session.execute(
        select(RefreshToken).where(RefreshToken.token == refresh_token_str)
    )
    db_token = result.scalars().first()
    assert db_token is not None
    assert db_token.is_revoked == False
    assert db_token.expires_at > datetime.now(timezone.utc)


@pytest.mark.asyncio
async def test_expired_refresh_token(db_session: AsyncSession):
    user = User(
        email="expired@example.com",
        hashed_password=security.get_password_hash("testpassword"),
        full_name="Expired User",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    refresh_token_str = security.create_refresh_token()

    db_refresh = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) - timedelta(hours=1),
    )
    db_session.add(db_refresh)
    await db_session.commit()

    result = await db_session.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token_str,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
    )
    db_token = result.scalars().first()
    assert db_token is None


@pytest.mark.asyncio
async def test_revoked_refresh_token(db_session: AsyncSession):
    user = User(
        email="revoked@example.com",
        hashed_password=security.get_password_hash("testpassword"),
        full_name="Revoked User",
        is_active=True,
    )
    db_session.add(user)
    await db_session.commit()
    await db_session.refresh(user)

    refresh_token_str = security.create_refresh_token()

    db_refresh = RefreshToken(
        token=refresh_token_str,
        user_id=user.id,
        expires_at=datetime.now(timezone.utc) + timedelta(days=7),
        is_revoked=True,
    )
    db_session.add(db_refresh)
    await db_session.commit()

    result = await db_session.execute(
        select(RefreshToken).where(
            RefreshToken.token == refresh_token_str,
            RefreshToken.is_revoked == False,
            RefreshToken.expires_at > datetime.now(timezone.utc),
        )
    )
    db_token = result.scalars().first()
    assert db_token is None


def test_password_hashing():
    password = "secretpassword"
    hashed = security.get_password_hash(password)
    assert security.verify_password(password, hashed) is True
    assert security.verify_password("wrongpassword", hashed) is False


def test_access_token_creation():
    user_id = str(uuid.uuid4())
    access_token = security.create_access_token(user_id, tenant_id=None)
    payload = jwt.decode(
        access_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert "sub" in payload
    assert payload["sub"] == user_id
    assert "exp" in payload
    assert "tenant_id" not in payload

    access_token_with_tenant = security.create_access_token(
        user_id, tenant_id="test-tenant-id"
    )
    payload_with_tenant = jwt.decode(
        access_token_with_tenant, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    assert payload_with_tenant["tenant_id"] == "test-tenant-id"


def test_token_expiration():
    user_id = str(uuid.uuid4())
    short_token = security.create_access_token(
        user_id, expires_delta=timedelta(minutes=1)
    )
    long_token = security.create_access_token(
        user_id, expires_delta=timedelta(hours=24)
    )

    short_payload = jwt.decode(
        short_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )
    long_payload = jwt.decode(
        long_token, settings.SECRET_KEY, algorithms=[settings.ALGORITHM]
    )

    assert short_payload["exp"] < long_payload["exp"]
