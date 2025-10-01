# app/schemas/payment.py
from pydantic import BaseModel, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .base import BaseSchema, DateTimeBase
from .tenant import TenantResponse
from .property import PropertyResponse

class PaymentStatus(str, Enum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

# Base schema
class RentPaymentBase(BaseSchema):
    amount: float = Field(..., gt=0)
    due_date: datetime
    period_start: datetime
    period_end: datetime
    currency: str = Field("KES", max_length=3)
    is_recurring: bool = True
    payment_method: str = Field("mpesa", max_length=20)
    reference_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    late_fee: float = Field(0.0, ge=0)

# Schema for creating a payment
class RentPaymentCreate(RentPaymentBase):
    tenant_id: int
    property_id: int

# Schema for updating a payment
class RentPaymentUpdate(BaseSchema):
    amount: Optional[float] = Field(None, gt=0)
    payment_status: Optional[PaymentStatus] = None
    mpesa_transaction_id: Optional[str] = Field(None, max_length=50)
    reference_number: Optional[str] = Field(None, max_length=50)
    notes: Optional[str] = None
    late_fee: Optional[float] = Field(None, ge=0)

# Schema for response
class RentPaymentResponse(RentPaymentBase, DateTimeBase):
    id: int
    tenant_id: int
    property_id: int
    payment_status: PaymentStatus
    mpesa_transaction_id: Optional[str] = None
    payment_date: Optional[datetime] = None
    tenant: Optional[TenantResponse] = None
    property: Optional[PropertyResponse] = None