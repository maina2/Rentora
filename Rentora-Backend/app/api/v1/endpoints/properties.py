from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Property
from app.schemas.property import Property, PropertyCreate
from app.core.auth import get_current_user
from typing import List
from app.db.models import Tenant

router = APIRouter(prefix="/properties", tags=["properties"])

@router.get("/", response_model=List[Property])
async def get_properties(
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    if user_type == "landlord":
        result = await db.execute(select(Property).filter(Property.landlord_id == user.id))
    else:
        result = await db.execute(select(Property).join(Tenant).filter(Tenant.id == user.id))
    properties = result.scalars().all()
    return properties

@router.post("/", response_model=Property)
async def create_property(
    property: PropertyCreate,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    if user_type != "landlord":
        raise HTTPException(status_code=403, detail="Only landlords can create properties")
    if property.landlord_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot create property for another landlord")
    db_property = Property(**property.dict())
    db.add(db_property)
    await db.commit()
    await db.refresh(db_property)
    return db_property

@router.get("/{property_id}", response_model=Property)
async def get_property(
    property_id: int,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    result = await db.execute(select(Property).filter(Property.id == property_id))
    property = result.scalars().first()
    if not property:
        raise HTTPException(status_code=404, detail="Property not found")
    if user_type == "landlord" and property.landlord_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this property")
    if user_type == "tenant":
        tenant_result = await db.execute(select(Tenant).filter(Tenant.id == user.id, Tenant.property_id == property_id))
        if not tenant_result.scalars().first():
            raise HTTPException(status_code=403, detail="Not authorized to view this property")
    return property