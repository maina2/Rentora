# app/schemas/__init__.py
from .base import BaseSchema, DateTimeBase
from .user import UserBase, UserCreate, UserUpdate, UserResponse, UserLogin, Token, TokenData, Role
from .landlord import LandlordBase, LandlordCreate, LandlordUpdate, LandlordResponse, LandlordWithProperties
from .property import PropertyBase, PropertyCreate, PropertyUpdate, PropertyResponse, PropertyWithRelations
from .tenant import TenantBase, TenantCreate, TenantUpdate, TenantResponse, TenantWithRelations
from .payment import RentPaymentBase, RentPaymentCreate, RentPaymentUpdate, RentPaymentResponse, PaymentStatus
from .notification import NotificationBase, NotificationCreate, NotificationUpdate, NotificationResponse, NotificationPriority
from .lease import LeaseAgreementBase, LeaseAgreementCreate, LeaseAgreementUpdate, LeaseAgreementResponse
from .maintenance import MaintenanceRequestBase, MaintenanceRequestCreate, MaintenanceRequestUpdate, MaintenanceRequestResponse

__all__ = [
    'BaseSchema', 'DateTimeBase',
    'UserBase', 'UserCreate', 'UserUpdate', 'UserResponse', 'UserLogin', 'Token', 'TokenData', 'Role',
    'LandlordBase', 'LandlordCreate', 'LandlordUpdate', 'LandlordResponse', 'LandlordWithProperties',
    'PropertyBase', 'PropertyCreate', 'PropertyUpdate', 'PropertyResponse', 'PropertyWithRelations',
    'TenantBase', 'TenantCreate', 'TenantUpdate', 'TenantResponse', 'TenantWithRelations',
    'RentPaymentBase', 'RentPaymentCreate', 'RentPaymentUpdate', 'RentPaymentResponse', 'PaymentStatus',
    'NotificationBase', 'NotificationCreate', 'NotificationUpdate', 'NotificationResponse', 'NotificationPriority',
    'LeaseAgreementBase', 'LeaseAgreementCreate', 'LeaseAgreementUpdate', 'LeaseAgreementResponse',
    'MaintenanceRequestBase', 'MaintenanceRequestCreate', 'MaintenanceRequestUpdate', 'MaintenanceRequestResponse'
]