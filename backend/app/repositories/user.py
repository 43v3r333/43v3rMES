from backend.app.repositories.base import BaseRepository
from backend.app.models.tenant import User
from backend.app.schemas.user import UserCreate, UserUpdate
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from typing import Optional

class UserRepository(BaseRepository[User, UserCreate, UserUpdate]):
    async def get_by_email(self, db: AsyncSession, *, email: str) -> Optional[User]:
        result = await db.execute(select(User).where(User.email == email, User.is_deleted == False))
        return result.scalars().first()

user = UserRepository(User)
