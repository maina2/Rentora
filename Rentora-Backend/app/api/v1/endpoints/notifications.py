from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Notification, Tenant
from app.schemas.notification import Notification, NotificationCreate
from app.core.auth import get_current_user
from typing import List

router = APIRouter(prefix="/notifications", tags=["notifications"])

@router.get("/", response_model=List[Notification])
async def get_notifications(
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    result = await db.execute(
        select(Notification).filter(
            Notification.recipient_type == user_type,
            Notification.recipient_id == user.id
        )
    )
    notifications = result.scalars().all()
    return notifications

@router.post("/", response_model=Notification)
async def create_notification(
    notification: NotificationCreate,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    if user_type != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can create notifications")
    if notification.recipient_type == "tenant":
        tenant_result = await db.execute(
            select(Tenant).filter(
                Tenant.id == notification.recipient_id,
                Tenant.landlord_id == user.id
            )
        )
        if not tenant_result.scalars().first():
            raise HTTPException(status_code=403, detail="Not authorized to notify this tenant")
    db_notification = Notification(**notification.dict())
    db.add(db_notification)
    await db.commit()
    await db.refresh(db_notification)
    return db_notification

@router.get("/{notification_id}", response_model=Notification)
async def get_notification(
    notification_id: int,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    result = await db.execute(select(Notification).filter(Notification.id == notification_id))
    notification = result.scalars().first()
    if not notification:
        raise HTTPException(status_code=404, detail="Notification not found")
    if (notification.recipient_type != user_type or
            notification.recipient_id != user.id):
        raise HTTPException(status_code=403, detail="Not authorized to view this notification")
    return notification