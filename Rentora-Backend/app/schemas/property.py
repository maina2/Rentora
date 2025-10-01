# app/schemas/property.py
from pydantic import BaseModel, Field
from typing import Optional, List
from datetime import datetime
from .base import BaseSchema, DateTimeBase
from .landlord import LandlordResponse

# Base schema
class PropertyBase(BaseSchema):
    address: str = Field(..., max_length=200)
    city: str = Field(..., max_length=100)
    estate: Optional[str] = Field(None, max_length=100)
    property_type: str = Field(..., max_length=50)
    total_units: int = Field(1, ge=1)
    description: Optional[str] = None
    rent_amount: float = Field(..., gt=0)
    security_deposit: float = Field(0.0, ge=0)
    property_size: Optional[str] = Field(None, max_length=50)
    amenities: Optional[str] = None
    is_available: bool = True
    available_from: Optional[datetime] = None

# Schema for creating a property
class PropertyCreate(PropertyBase):
    landlord_id: int

# Schema for updating a property
class PropertyUpdate(BaseSchema):
    address: Optional[str] = Field(None, max_length=200)
    city: Optional[str] = Field(None, max_length=100)
    estate: Optional[str] = Field(None, max_length=100)
    property_type: Optional[str] = Field(None, max_length=50)
    total_units: Optional[int] = Field(None, ge=1)
    description: Optional[str] = None
    rent_amount: Optional[float] = Field(None, gt=0)
    security_deposit: Optional[float] = Field(None, ge=0)
    property_size: Optional[str] = Field(None, max_length=50)
    amenities: Optional[str] = None
    is_available: Optional[bool] = None
    available_from: Optional[datetime] = None

# Schema for response
class PropertyResponse(PropertyBase, DateTimeBase):
    id: int
    landlord_id: int
    landlord: Optional[LandlordResponse] = None

# Schema with relationships
class PropertyWithRelations(PropertyResponse):
    tenants: list = []         
    payments: list = []       
    leases: list = []          
    maintenance_requests: list = [] 