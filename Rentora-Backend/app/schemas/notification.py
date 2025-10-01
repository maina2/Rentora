# app/schemas/notification.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .base import BaseSchema, DateTimeBase

class NotificationPriority(str, Enum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

# Base schema
class NotificationBase(BaseSchema):
    recipient_type: str = Field(..., max_length=10)  # 'landlord' or 'tenant'
    title: str = Field(..., max_length=200)
    message: str
    notification_type: str = Field(..., max_length=50)
    priority: NotificationPriority = NotificationPriority.NORMAL
    action_url: Optional[str] = Field(None, max_length=200)
    expires_at: Optional[datetime] = None
    related_entity_type: Optional[str] = Field(None, max_length=50)
    related_entity_id: Optional[int] = None

# Schema for creating a notification
class NotificationCreate(NotificationBase):
    recipient_id: int
    delivery_method: str = Field("in-app", max_length=20)

# Schema for updating a notification
class NotificationUpdate(BaseSchema):
    is_read: Optional[bool] = None

# Schema for response
class NotificationResponse(NotificationBase, DateTimeBase):
    id: int
    recipient_id: int
    delivery_method: str
    is_read: bool