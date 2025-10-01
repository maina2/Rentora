from fastapi import APIRouter
from .endpoints import landlords, tenants, properties, payments, notifications, auth, admin

api_router = APIRouter(prefix="/v1")
api_router.include_router(landlords.router)
api_router.include_router(tenants.router)
api_router.include_router(properties.router)
api_router.include_router(payments.router)
api_router.include_router(notifications.router)
api_router.include_router(auth.router)
api_router.include_router(admin.router)