# app/schemas/landlord.py
from pydantic import BaseModel, Field
from typing import Optional
from .base import BaseSchema, DateTimeBase
from .user import UserResponse

# Base schema
class LandlordBase(BaseSchema):
    business_name: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    bank_account: Optional[str] = Field(None, max_length=50)
    kra_pin: Optional[str] = Field(None, max_length=20)

# Schema for creating a landlord
class LandlordCreate(LandlordBase):
    user_id: int

# Schema for updating a landlord
class LandlordUpdate(BaseSchema):
    business_name: Optional[str] = Field(None, max_length=100)
    tax_id: Optional[str] = Field(None, max_length=50)
    bank_account: Optional[str] = Field(None, max_length=50)
    kra_pin: Optional[str] = Field(None, max_length=20)

# Schema for response
class LandlordResponse(LandlordBase, DateTimeBase):
    id: int
    user_id: int
    user: Optional[UserResponse] = None

# Schema with relationships
class LandlordWithProperties(LandlordResponse):
    properties: list = []  # Will be populated with PropertyResponse
    tenants: list = []     # Will be populated with TenantResponse