from typing import List, Optional
from uuid import UUID
from sqlalchemy import select, and_
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.repositories.base import BaseRepository
from backend.app.modules.notifications.models.notification import Notification, EscalationRule
from backend.app.modules.notifications.schemas.notification import NotificationCreate, EscalationRuleCreate
from typing import Any
class NotificationRepository(BaseRepository[Notification, NotificationCreate, Any]):
    async def get_unread_by_user(self, db: AsyncSession, user_id: UUID) -> List[Notification]:
        result = await db.execute(
            select(Notification).where(Notification.user_id == user_id, Notification.is_read == False)
        )
        return result.scalars().all()

class EscalationRuleRepository(BaseRepository[EscalationRule, EscalationRuleCreate, Any]):
    async def get_active_by_tenant(self, db: AsyncSession, tenant_id: UUID) -> List[EscalationRule]:
        result = await db.execute(
            select(EscalationRule).where(EscalationRule.tenant_id == tenant_id, EscalationRule.is_active == True)
        )
        return result.scalars().all()

notification_repo = NotificationRepository(Notification)
rule_repo = EscalationRuleRepository(EscalationRule)
