from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
from ..db import get_db
from ..core.security import get_current_user
from ..schemas import Transaction, TransactionOut
from ..models import Transaction as TransactionModel, Merchant as MerchantModel

router = APIRouter()


@router.post("/transactions", response_model=TransactionOut, status_code=201)
async def create_transaction(payload: Transaction, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    user_id = user.get("username")
    if not user_id:
        raise HTTPException(status_code=401, detail="Invalid authentication credentials")
    # Ensure merchant exists or create a placeholder merchant record
    q = select(MerchantModel).where(MerchantModel.id == payload.merchant_id)
    res = await db.execute(q)
    merchant = res.scalars().first()
    if not merchant:
        merchant = MerchantModel(id=payload.merchant_id, name=f"merchant-{payload.merchant_id}")
        db.add(merchant)
        await db.flush()

    txn = TransactionModel(
        merchant_id=payload.merchant_id,
        user_id=user_id,
        amount=payload.amount,
        currency=payload.currency,
        type=payload.type,
    )
    db.add(txn)
    await db.flush()
    await db.commit()
    await db.refresh(txn)
    return TransactionOut(id=txn.id, merchant_id=txn.merchant_id, user_id=txn.user_id, amount=txn.amount, currency=txn.currency, type=txn.type, timestamp=txn.timestamp)


@router.get("/transactions/merchant/{merchant_id}", response_model=List[TransactionOut])
async def list_transactions_for_merchant(merchant_id: int, limit: int = Query(50, ge=1, le=100), db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    user_id = user.get("username")
    q = select(TransactionModel).where(TransactionModel.merchant_id == merchant_id, TransactionModel.user_id == user_id).order_by(TransactionModel.timestamp.desc()).limit(limit)
    res = await db.execute(q)
    txns = res.scalars().all()
    return [TransactionOut(id=t.id, merchant_id=t.merchant_id, user_id=t.user_id, amount=t.amount, currency=t.currency, type=t.type, timestamp=t.timestamp) for t in txns]
