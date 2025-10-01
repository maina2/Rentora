from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import insert, select, delete
from app.db.session import get_db
from app.db.models import User, Landlord, Tenant, Property, RentPayment
from app.schemas.user import UserCreate, UserOut
from app.core.permissions import get_admin_user
from app.core.auth import pwd_context
from typing import List

router = APIRouter(prefix="/admin", tags=["admin"])

@router.post("/users", response_model=UserOut)
async def create_user(user: UserCreate, db: AsyncSession = Depends(get_db), admin: User = Depends(get_admin_user)):
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user_data = {
        "email": user.email,
        "password_hash": pwd_context.hash(user.password),
        "role": user.role or "tenant",
        "is_active": True
    }
    result = await db.execute(insert(User).values(**user_data))
    user_id = result.inserted_primary_key[0]
    
    if user_data["role"] == "landlord":
        landlord_data = {"user_id": user_id, "name": user.name, "phone": user.phone}
        await db.execute(insert(Landlord).values(**landlord_data))
    elif user_data["role"] == "tenant":
        tenant_data = {
            "user_id": user_id,
            "name": user.name,
            "phone": user.phone,
            "landlord_id": admin.id  # Default to admin's ID, adjust as needed
        }
        await db.execute(insert(Tenant).values(**tenant_data))
    
    await db.commit()
    result = await db.execute(select(User).filter(User.id == user_id))
    return result.scalars().first()

@router.get("/users", response_model=List[UserOut])
async def list_users(db: AsyncSession = Depends(get_db), admin: User = Depends(get_admin_user)):
    result = await db.execute(select(User))
    return result.scalars().all()

@router.delete("/users/{user_id}")
async def delete_user(user_id: int, db: AsyncSession = Depends(get_db), admin: User = Depends(get_admin_user)):
    result = await db.execute(select(User).filter(User.id == user_id))
    if not result.scalars().first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="User not found")
    await db.execute(delete(User).filter(User.id == user_id))
    await db.commit()
    return {"message": "User deleted"}