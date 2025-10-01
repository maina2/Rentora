from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from app.db.session import get_db
from app.db.models import RentPayment, Tenant
from app.schemas.payment import RentPayment, RentPaymentCreate
from app.core.auth import get_current_user
from typing import List

router = APIRouter(prefix="/payments", tags=["payments"])

@router.get("/", response_model=List[RentPayment])
async def get_payments(
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    if user_type == "landlord":
        result = await db.execute(select(RentPayment).join(Tenant).filter(Tenant.landlord_id == user.id))
    else:
        result = await db.execute(select(RentPayment).filter(RentPayment.tenant_id == user.id))
    payments = result.scalars().all()
    return payments

@router.post("/", response_model=RentPayment)
async def create_payment(
    payment: RentPaymentCreate,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    if user_type != "tenant":
        raise HTTPException(status_code=403, detail="Only tenants can create payments")
    if payment.tenant_id != user.id:
        raise HTTPException(status_code=403, detail="Cannot create payment for another tenant")
    db_payment = RentPayment(**payment.dict())
    db.add(db_payment)
    await db.commit()
    await db.refresh(db_payment)
    return db_payment

@router.get("/{payment_id}", response_model=RentPayment)
async def get_payment(
    payment_id: int,
    current_user: tuple = Depends(get_current_user),
    db: AsyncSession = Depends(get_db)
):
    user, user_type = current_user
    result = await db.execute(select(RentPayment).filter(RentPayment.id == payment_id))
    payment = result.scalars().first()
    if not payment:
        raise HTTPException(status_code=404, detail="Payment not found")
    if user_type == "tenant" and payment.tenant_id != user.id:
        raise HTTPException(status_code=403, detail="Not authorized to view this payment")
    if user_type == "landlord":
        tenant_result = await db.execute(select(Tenant).filter(Tenant.id == payment.tenant_id, Tenant.landlord_id == user.id))
        if not tenant_result.scalars().first():
            raise HTTPException(status_code=403, detail="Not authorized to view this payment")
    return payment