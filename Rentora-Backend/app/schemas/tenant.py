# app/schemas/tenant.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseSchema, DateTimeBase
from .user import UserResponse
from .landlord import LandlordResponse
from .property import PropertyResponse

# Base schema
class TenantBase(BaseSchema):
    emergency_contact: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    id_number: Optional[str] = Field(None, max_length=20)
    lease_start_date: Optional[datetime] = None
    lease_end_date: Optional[datetime] = None

# Schema for creating a tenant
class TenantCreate(TenantBase):
    user_id: int
    landlord_id: int
    property_id: Optional[int] = None

# Schema for updating a tenant
class TenantUpdate(BaseSchema):
    emergency_contact: Optional[str] = Field(None, max_length=100)
    emergency_contact_phone: Optional[str] = Field(None, max_length=20)
    id_number: Optional[str] = Field(None, max_length=20)
    lease_start_date: Optional[datetime] = None
    lease_end_date: Optional[datetime] = None
    property_id: Optional[int] = None

# Schema for response
class TenantResponse(TenantBase, DateTimeBase):
    id: int
    user_id: int
    landlord_id: int
    property_id: Optional[int] = None
    user: Optional[UserResponse] = None
    landlord: Optional[LandlordResponse] = None
    property: Optional[PropertyResponse] = None

# Schema with relationships
class TenantWithRelations(TenantResponse):
    payments: list = []
    leases: list = []
    maintenance_requests: list = []