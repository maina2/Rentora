from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import Landlord, User
from app.schemas.user import LandlordOut
from app.core.permissions import get_admin_user, get_landlord_user
from typing import List

router = APIRouter(prefix="/landlords", tags=["landlords"])

@router.get("/", response_model=List[LandlordOut])
async def get_landlords(
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_admin_user)  # Admins can view all landlords
):
    result = await db.execute(select(Landlord))
    landlords = result.scalars().all()
    return landlords

@router.get("/{landlord_id}", response_model=LandlordOut)
async def get_landlord(
    landlord_id: int,
    db: AsyncSession = Depends(get_db),
    current_user: User = Depends(get_landlord_user)
):
    result = await db.execute(select(Landlord).filter(Landlord.id == landlord_id))
    landlord = result.scalars().first()
    if not landlord:
        raise HTTPException(status_code=404, detail="Landlord not found")
    if current_user.role != "admin" and landlord.user_id != current_user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this landlord")
    return landlord