from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy import select
import csv
import io
from fastapi.responses import StreamingResponse
from ..db import get_db
from ..core.security import get_current_user
from ..models import Consent as ConsentModel, Transaction as TransactionModel
from ..schemas import ConsentIn, ConsentOut

router = APIRouter()


@router.post("/consents", response_model=ConsentOut, status_code=201)
async def create_consent(payload: ConsentIn, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    consent = ConsentModel(user_id=payload.user_id, merchant_id=payload.merchant_id, scope=payload.scope)
    db.add(consent)
    await db.flush()
    await db.commit()
    await db.refresh(consent)
    return ConsentOut(id=consent.id, user_id=consent.user_id, merchant_id=consent.merchant_id, scope=consent.scope, granted_at=consent.granted_at)


@router.get("/export/merchant/{merchant_id}")
async def export_transactions_csv(merchant_id: int, db: AsyncSession = Depends(get_db), user=Depends(get_current_user)):
    # require consent for the current user and merchant
    q = select(ConsentModel).where(ConsentModel.user_id == user.get("username"), ConsentModel.merchant_id == merchant_id)
    res = await db.execute(q)
    consent = res.scalars().first()
    if not consent:
        raise HTTPException(status_code=403, detail="No consent for export")

    q2 = select(TransactionModel).where(TransactionModel.merchant_id == merchant_id).order_by(TransactionModel.timestamp.desc())
    res2 = await db.execute(q2)
    txns = res2.scalars().all()

    def iter_csv():
        buf = io.StringIO()
        writer = csv.writer(buf)
        writer.writerow(["id", "merchant_id", "user_id", "amount", "currency", "type", "timestamp"]) 
        yield buf.getvalue()
        buf.seek(0)
        buf.truncate(0)
        for t in txns:
            writer.writerow([t.id, t.merchant_id, t.user_id, float(t.amount), t.currency, t.type, t.timestamp.isoformat()])
            yield buf.getvalue()
            buf.seek(0)
            buf.truncate(0)

    return StreamingResponse(iter_csv(), media_type="text/csv")
