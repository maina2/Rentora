from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select, insert
from app.db.session import get_db
from app.db.models import User
from app.core.auth import oauth2_scheme, pwd_context, create_access_token
from app.schemas.user import UserCreate
from pydantic import BaseModel

router = APIRouter(prefix="/auth", tags=["auth"])

class LoginRequest(BaseModel):
    email: str
    password: str

@router.post("/login")
async def login(form_data: LoginRequest, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == form_data.email))
    user = result.scalars().first()
    if not user or not pwd_context.verify(form_data.password, user.password_hash):
        raise HTTPException(status_code=401, detail="Invalid credentials")
    access_token = create_access_token(data={"sub": user.email, "role": user.role})
    return {"access_token": access_token, "token_type": "bearer"}

@router.post("/users/admin", status_code=status.HTTP_201_CREATED)
async def create_admin_user(user: UserCreate, db: AsyncSession = Depends(get_db)):
    result = await db.execute(select(User).filter(User.email == user.email))
    if result.scalars().first():
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail="Email already registered")
    
    user_data = {
        "email": user.email,
        "password_hash": pwd_context.hash(user.password),
        "role": "admin",
        "is_active": True
    }
    result = await db.execute(insert(User).values(**user_data))
    await db.commit()
    return {"message": "Admin user created successfully"}