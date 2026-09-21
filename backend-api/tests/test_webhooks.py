import os
import json
from datetime import datetime, timezone
import pytest
from httpx import AsyncClient
from httpx import ASGITransport


@pytest.mark.asyncio
async def test_mobile_money_webhook(tmp_path, anyio_backend="asyncio"):
    from app.main import app

    signature_secret = "dev-secret"
    payload = {"transaction_id": "tx-123", "amount": 1000, "timestamp": datetime.now(timezone.utc).isoformat()}
    raw = json.dumps(payload).encode()
    import hmac, hashlib

    sig = hmac.new(signature_secret.encode(), raw, hashlib.sha256).hexdigest()

    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        resp = await ac.post("/api/webhooks/mobile-money", content=raw, headers={"x-signature": sig})
        assert resp.status_code == 200
        assert resp.json()["status"] in ("accepted", "already_processed")
