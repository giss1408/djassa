from fastapi import APIRouter, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..schemas import Payment, PaymentOut
from ..db import get_db
from ..core.security import get_current_user
from ..models import Payment as PaymentModel

router = APIRouter()


@router.post("/payments", response_model=PaymentOut, status_code=201)
async def create_payment(payload: Payment, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # Simple DB insert using SQLAlchemy ORM
    new = PaymentModel(amount=payload.amount, currency=payload.currency, recipient_id=payload.recipient_id)
    db.add(new)
    await db.flush()
    await db.commit()
    await db.refresh(new)
    return PaymentOut(id=new.id, amount=float(new.amount), currency=new.currency, recipient_id=new.recipient_id)
