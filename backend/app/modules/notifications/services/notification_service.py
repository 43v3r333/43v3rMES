from typing import List, Any
from uuid import UUID
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.modules.notifications.models.notification import Notification
from backend.app.modules.notifications.schemas.notification import NotificationCreate
from backend.app.models.tenant import User

class NotificationService:
    async def notify_user(self, db: AsyncSession, user_id: UUID, tenant_id: UUID, title: str, message: str, type: str = "SYSTEM", severity: str = "INFO") -> Notification:
        db_obj = Notification(
            user_id=user_id,
            tenant_id=tenant_id,
            title=title,
            message=message,
            type=type,
            severity=severity
        )
        db.add(db_obj)
        await db.commit()
        await db.refresh(db_obj)
        return db_obj

    async def mark_as_read(self, db: AsyncSession, notification_id: UUID, user_id: UUID):
        from sqlalchemy import update
        await db.execute(
            update(Notification).where(Notification.id == notification_id, Notification.user_id == user_id).values(is_read=True)
        )
        await db.commit()

notification_service = NotificationService()
