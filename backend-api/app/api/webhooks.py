from fastapi import APIRouter, Request, Header, HTTPException, Depends
from sqlalchemy.ext.asyncio import AsyncSession
from ..db import get_db
from ..models import WebhookEvent, WebhookIdempotency
from ..schemas.webhook import WebhookIn
import hmac
import hashlib
import json
from datetime import datetime, timedelta
import os

REPLAY_WINDOW_SECONDS = int(os.getenv("WEBHOOK_REPLAY_WINDOW", "300"))

router = APIRouter(prefix="/api/webhooks", tags=["webhooks"])


async def verify_signature(raw_body: bytes, signature: str, secret: str) -> bool:
    if not signature:
        return False
    mac = hmac.new(secret.encode(), raw_body, hashlib.sha256).hexdigest()
    return hmac.compare_digest(mac, signature)


@router.post("/mobile-money")
@router.post("/mobile-money")
@limiter.limit("10/minute", key_func=lambda: "webhook")
async def mobile_money_webhook(
    request: Request,
    x_signature: str | None = Header(None),
    db: AsyncSession = Depends(get_db),
):
    raw = await request.body()
    try:
        payload = json.loads(raw)
    except Exception:
        raise HTTPException(status_code=400, detail="invalid json")

    # Secret should be stored in secrets manager; fallback to env for dev
    secret = os.getenv("MOBILE_MONEY_SECRET", "dev-secret")

    ok = await verify_signature(raw, x_signature or "", secret)
    if not ok:
        raise HTTPException(status_code=401, detail="invalid signature")

    # idempotency: check unique external_id
    external_id = payload.get("transaction_id") or payload.get("id")
    if not external_id:
        raise HTTPException(status_code=400, detail="missing transaction id")

    # Basic replay protection: require a `timestamp` field within allowed window
    ts = payload.get("timestamp")
    if ts:
        try:
            ev_time = datetime.fromisoformat(ts)
            now = datetime.utcnow()
            if abs((now - ev_time).total_seconds()) > REPLAY_WINDOW_SECONDS:
                raise HTTPException(status_code=400, detail="replay window exceeded")
        except Exception:
            raise HTTPException(status_code=400, detail="invalid timestamp")

    existing = await db.get(WebhookIdempotency, external_id)
    if existing:
        return {"status": "already_processed"}

    # persist idempotency marker and event
    marker = WebhookIdempotency(external_id=external_id)
    event = WebhookEvent(payload=json.dumps(payload), external_id=external_id)
    db.add(marker)
    db.add(event)
    await db.commit()

    # Enqueue async processing via Celery
    try:
        from ..celery_tasks import send_webhook_processing_event
        send_webhook_processing_event.delay(external_id)
    except Exception:
        # fallback: process inline
        from ..services import tontine
        await tontine.process_webhook(external_id)

    return {"status": "accepted"}
