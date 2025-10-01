# app/schemas/base.py
from pydantic import BaseModel
from typing import Optional
from datetime import datetime

class BaseSchema(BaseModel):
    class Config:
        from_attributes = True
        arbitrary_types_allowed = True

class DateTimeBase(BaseSchema):
    created_at: Optional[datetime] = None