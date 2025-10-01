# app/schemas/user.py
from pydantic import BaseModel, EmailStr, Field
from typing import Optional
from datetime import datetime
from enum import Enum
from .base import BaseSchema, DateTimeBase

class Role(str, Enum):
    ADMIN = "ADMIN"
    LANDLORD = "LANDLORD"
    TENANT = "TENANT"

# Base schema with common fields
class UserBase(BaseSchema):
    email: EmailStr
    role: Role
    full_name: str = Field(..., min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)

# Schema for creating a user
class UserCreate(UserBase):
    password: str = Field(..., min_length=6)

# Schema for updating a user
class UserUpdate(BaseSchema):
    email: Optional[EmailStr] = None
    full_name: Optional[str] = Field(None, min_length=1, max_length=100)
    phone: Optional[str] = Field(None, max_length=20)
    is_active: Optional[bool] = None

# Schema for response (without password)
class UserResponse(UserBase, DateTimeBase):
    id: int
    is_active: bool
    profile_id: Optional[int] = None
    profile_type: Optional[str] = None

# Schema for authentication
class UserLogin(BaseModel):
    email: EmailStr
    password: str

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    email: Optional[str] = None