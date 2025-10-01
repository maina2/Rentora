# app/schemas/maintenance.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseSchema, DateTimeBase
from .tenant import TenantResponse
from .property import PropertyResponse

# Base schema
class MaintenanceRequestBase(BaseSchema):
    title: str = Field(..., max_length=200)
    description: str
    priority: str = Field("medium", max_length=20)  # low, medium, high, emergency
    status: str = Field("pending", max_length=20)   # pending, in_progress, completed

# Schema for creating a maintenance request
class MaintenanceRequestCreate(MaintenanceRequestBase):
    tenant_id: int
    property_id: int

# Schema for updating a maintenance request
class MaintenanceRequestUpdate(BaseSchema):
    title: Optional[str] = Field(None, max_length=200)
    description: Optional[str] = None
    priority: Optional[str] = Field(None, max_length=20)
    status: Optional[str] = Field(None, max_length=20)
    completed_at: Optional[datetime] = None
    cost: Optional[float] = Field(None, ge=0)
    assigned_to: Optional[str] = Field(None, max_length=100)

# Schema for response
class MaintenanceRequestResponse(MaintenanceRequestBase, DateTimeBase):
    id: int
    tenant_id: int
    property_id: int
    created_at: datetime
    completed_at: Optional[datetime] = None
    cost: Optional[float] = None
    assigned_to: Optional[str] = None
    tenant: Optional[TenantResponse] = None
    property: Optional[PropertyResponse] = None