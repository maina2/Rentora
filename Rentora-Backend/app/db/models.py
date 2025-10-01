from sqlalchemy import Boolean, Column, Enum, Integer, String, Float, ForeignKey, DateTime, Text
from sqlalchemy.orm import relationship
from sqlalchemy.sql import func
from app.db.base import Base
from enum import Enum as PyEnum

class PaymentStatus(PyEnum):
    PENDING = "pending"
    COMPLETED = "completed"
    FAILED = "failed"
    REFUNDED = "refunded"

class Role(PyEnum):
    ADMIN = "ADMIN"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"

class NotificationPriority(PyEnum):
    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    URGENT = "urgent"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, nullable=False, index=True)
    password_hash = Column(String, nullable=False)
    role = Column(Enum(Role), nullable=False)
    is_active = Column(Boolean, default=True)
    created_at = Column(DateTime, server_default=func.now())
    full_name = Column(String, nullable=False)
    phone = Column(String, nullable=True)
    profile_id = Column(Integer, nullable=True)
    profile_type = Column(String, nullable=True)

class Landlord(Base):
    __tablename__ = "landlords"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    business_name = Column(String, nullable=True)
    tax_id = Column(String, nullable=True)
    bank_account = Column(String, nullable=True)
    kra_pin = Column(String, nullable=True)
    user = relationship("User")
    properties = relationship("Property", back_populates="landlord")
    tenants = relationship("Tenant", back_populates="landlord")

class Property(Base):
    __tablename__ = "properties"

    id = Column(Integer, primary_key=True, index=True)
    address = Column(String, nullable=False)
    city = Column(String, nullable=False)
    estate = Column(String, nullable=True)
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    created_at = Column(DateTime, server_default=func.now())
    property_type = Column(String, nullable=False)
    total_units = Column(Integer, default=1)
    description = Column(Text, nullable=True)
    rent_amount = Column(Float, nullable=False)
    security_deposit = Column(Float, default=0.0)
    property_size = Column(String, nullable=True)
    amenities = Column(Text, nullable=True)
    is_available = Column(Boolean, default=True)
    available_from = Column(DateTime, nullable=True)
    landlord = relationship("Landlord", back_populates="properties")
    tenants = relationship("Tenant", back_populates="property")
    payments = relationship("RentPayment", back_populates="property")
    leases = relationship("LeaseAgreement", back_populates="property")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="property")

class Tenant(Base):
    __tablename__ = "tenants"

    id = Column(Integer, primary_key=True, index=True)
    user_id = Column(Integer, ForeignKey("users.id"), nullable=False, unique=True)
    landlord_id = Column(Integer, ForeignKey("landlords.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=True)
    emergency_contact = Column(String, nullable=True)
    emergency_contact_phone = Column(String, nullable=True)
    id_number = Column(String, nullable=True)
    lease_start_date = Column(DateTime, nullable=True)
    lease_end_date = Column(DateTime, nullable=True)
    user = relationship("User")
    landlord = relationship("Landlord", back_populates="tenants")
    property = relationship("Property", back_populates="tenants")
    payments = relationship("RentPayment", back_populates="tenant")
    leases = relationship("LeaseAgreement", back_populates="tenant")
    maintenance_requests = relationship("MaintenanceRequest", back_populates="tenant")

class RentPayment(Base):
    __tablename__ = "rent_payments"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    mpesa_transaction_id = Column(String, unique=True, nullable=True)
    payment_date = Column(DateTime, server_default=func.now())
    created_at = Column(DateTime, server_default=func.now())
    payment_method = Column(String, default="mpesa")
    payment_status = Column(Enum(PaymentStatus), default=PaymentStatus.PENDING)
    due_date = Column(DateTime, nullable=False)
    late_fee = Column(Float, default=0.0)
    reference_number = Column(String, nullable=True)
    notes = Column(Text, nullable=True)
    period_start = Column(DateTime, nullable=False)
    period_end = Column(DateTime, nullable=False)
    currency = Column(String, default="KES")
    is_recurring = Column(Boolean, default=True)
    tenant = relationship("Tenant", back_populates="payments")
    property = relationship("Property", back_populates="payments")

class Notification(Base):
    __tablename__ = "notifications"

    id = Column(Integer, primary_key=True, index=True)
    recipient_type = Column(String, nullable=False)
    recipient_id = Column(Integer, nullable=False, index=True)
    title = Column(String, nullable=False)
    message = Column(Text, nullable=False)
    notification_type = Column(String, nullable=False)
    delivery_method = Column(String, default="in-app")
    is_read = Column(Boolean, default=False)
    created_at = Column(DateTime, server_default=func.now())
    priority = Column(Enum(NotificationPriority), default=NotificationPriority.NORMAL)
    action_url = Column(String, nullable=True)
    expires_at = Column(DateTime, nullable=True)
    related_entity_type = Column(String, nullable=True)
    related_entity_id = Column(Integer, nullable=True)

class LeaseAgreement(Base):
    __tablename__ = "lease_agreements"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    start_date = Column(DateTime, nullable=False)
    end_date = Column(DateTime, nullable=False)
    monthly_rent = Column(Float, nullable=False)
    security_deposit = Column(Float, default=0.0)
    terms = Column(Text, nullable=True)
    status = Column(String, default="active")
    created_at = Column(DateTime, server_default=func.now())
    signed_date = Column(DateTime, nullable=True)
    document_path = Column(String, nullable=True)
    tenant = relationship("Tenant", back_populates="leases")
    property = relationship("Property", back_populates="leases")

class MaintenanceRequest(Base):
    __tablename__ = "maintenance_requests"

    id = Column(Integer, primary_key=True, index=True)
    tenant_id = Column(Integer, ForeignKey("tenants.id"), nullable=False)
    property_id = Column(Integer, ForeignKey("properties.id"), nullable=False)
    title = Column(String, nullable=False)
    description = Column(Text, nullable=False)
    priority = Column(String, default="medium")
    status = Column(String, default="pending")
    created_at = Column(DateTime, server_default=func.now())
    completed_at = Column(DateTime, nullable=True)
    cost = Column(Float, nullable=True)
    assigned_to = Column(String, nullable=True)
    tenant = relationship("Tenant", back_populates="maintenance_requests")
    property = relationship("Property", back_populates="maintenance_requests")