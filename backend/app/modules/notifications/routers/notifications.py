from typing import Any, List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from backend.app.api import deps
from backend.app.modules.notifications.repositories.notification_repo import notification_repo
from backend.app.modules.notifications.services.notification_service import notification_service
from backend.app.modules.notifications.schemas.notification import Notification
from backend.app.models.tenant import User
import uuid

router = APIRouter()

@router.get("/", response_model=List[Notification])
async def read_notifications(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    # Get all notifications for user
    from sqlalchemy import select
    from backend.app.modules.notifications.models.notification import Notification as NotificationModel
    result = await db.execute(
        select(NotificationModel).where(NotificationModel.user_id == current_user.id).order_by(NotificationModel.created_at.desc())
    )
    return result.scalars().all()

@router.post("/{notification_id}/read")
async def mark_notification_read(
    notification_id: uuid.UUID,
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    await notification_service.mark_as_read(db, notification_id, current_user.id)
    return {"status": "success"}

@router.get("/unread-count")
async def get_unread_count(
    db: AsyncSession = Depends(deps.get_db),
    current_user: User = Depends(deps.get_current_active_user),
) -> Any:
    from sqlalchemy import func, select
    from backend.app.modules.notifications.models.notification import Notification as NotificationModel
    result = await db.execute(
        select(func.count(NotificationModel.id)).where(NotificationModel.user_id == current_user.id, NotificationModel.is_read == False)
    )
    return {"count": result.scalar() or 0}
