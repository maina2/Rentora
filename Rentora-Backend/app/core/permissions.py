from fastapi import Depends, HTTPException, status
from app.core.auth import get_current_user
from app.db.models import User

def get_admin_user(user: User = Depends(get_current_user)):
    if user.role != "ADMIN":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Admin access required"
        )
    return user

def get_landlord_user(user: User = Depends(get_current_user)):
    if user.role != "LANDLORD":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Landlord access required"
        )
    return user

def get_tenant_user(user: User = Depends(get_current_user)):
    if user.role != "TENANT":
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Tenant access required"
        )
    return user