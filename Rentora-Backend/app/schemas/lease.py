# app/schemas/lease.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from .base import BaseSchema, DateTimeBase
from .tenant import TenantResponse
from .property import PropertyResponse

# Base schema
class LeaseAgreementBase(BaseSchema):
    start_date: datetime
    end_date: datetime
    monthly_rent: float = Field(..., gt=0)
    security_deposit: float = Field(0.0, ge=0)
    terms: Optional[str] = None
    status: str = Field("active", max_length=20)

# Schema for creating a lease
class LeaseAgreementCreate(LeaseAgreementBase):
    tenant_id: int
    property_id: int

# Schema for updating a lease
class LeaseAgreementUpdate(BaseSchema):
    end_date: Optional[datetime] = None
    monthly_rent: Optional[float] = Field(None, gt=0)
    security_deposit: Optional[float] = Field(None, ge=0)
    terms: Optional[str] = None
    status: Optional[str] = Field(None, max_length=20)
    signed_date: Optional[datetime] = None
    document_path: Optional[str] = Field(None, max_length=200)

# Schema for response
class LeaseAgreementResponse(LeaseAgreementBase, DateTimeBase):
    id: int
    tenant_id: int
    property_id: int
    signed_date: Optional[datetime] = None
    document_path: Optional[str] = None
    tenant: Optional[TenantResponse] = None
    property: Optional[PropertyResponse] = None