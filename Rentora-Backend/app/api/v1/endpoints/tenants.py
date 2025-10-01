from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.db.session import get_db
from app.db.models import Tenant, User
from app.schemas.user import TenantCreate, TenantOut
from app.core.permissions import get_landlord_user, get_tenant_user
from app.core.auth import pwd_context
from typing import List

router = APIRouter(prefix="/tenants", tags=["tenants"])

@router.get("/", response_model=List[TenantOut])
async def get_tenants(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_landlord_user)
):
    result = await db.execute(select(Tenant).filter(Tenant.landlord_id == current_user.id))
    tenants = result.scalars().all()
    return tenants

@router.post("/", response_model=TenantOut)
async def create_tenant(
    tenant: TenantCreate,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_landlord_user)
):
    result = await db.execute(select(User).filter(User.email == tenant.email))
    if result.scalars().first():
        raise HTTPException(status_code=400, detail="Email already registered")
    
    user_data = {
        "email": tenant.email,
        "password_hash": pwd_context.hash(tenant.password),
        "role": "tenant",
        "is_active": True
    }
    result = await db.execute(insert(User).values(**user_data))
    user_id = result.inserted_primary_key[0]

    tenant_data = {
        "user_id": user_id,
        "name": tenant.name,
        "phone": tenant.phone,
        "landlord_id": current_user.id,
        "property_id": tenant.property_id,
        "emergency_contact": tenant.emergency_contact,
        "lease_start_date": tenant.lease_start_date
    }
    result = await db.execute(insert(Tenant).values(**tenant_data))
    await db.commit()
    
    result = await db.execute(select(Tenant).filter(Tenant.user_id == user_id))
    return result.scalars().first()

@router.get("/{tenant_id}", response_model=TenantOut)
async def get_tenant(
    tenant_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_landlord_user)  # Allow landlords or admins
):
    result = await db.execute(select(Tenant).filter(Tenant.id == tenant_id))
    tenant = result.scalars().first()
    if not tenant:
        raise HTTPException(status_code=404, detail="Tenant not found")
    if current_user.role != "admin" and tenant.landlord_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this tenant")
    return tenant