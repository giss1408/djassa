import pytest
from httpx import AsyncClient
from httpx import ASGITransport
from app.main import app
from app.core.security import create_access_token


@pytest.mark.asyncio
async def test_create_and_list_transactions():
    async with AsyncClient(transport=ASGITransport(app=app), base_url="http://test") as ac:
        token_resp = await ac.post("/api/token", data={"username": "demo", "password": "demo123"})
        assert token_resp.status_code == 200
        token = token_resp.json()["access_token"]

        # create a transaction
        r = await ac.post(
            "/api/transactions",
            json={"merchant_id": 1, "user_id": "u1", "amount": 25.0, "currency": "XOF", "type": "sale"},
            headers={"Authorization": f"Bearer {token}"},
        )
        assert r.status_code == 201
        tx = r.json()
        assert tx["merchant_id"] == 1
        assert tx["user_id"] == "demo"

        # list transactions
        r2 = await ac.get("/api/transactions/merchant/1", headers={"Authorization": f"Bearer {token}"})
        assert r2.status_code == 200
        items = r2.json()
        assert isinstance(items, list)
        assert len(items) >= 1

        other_token = create_access_token({"sub": "other-user"})
        other_response = await ac.get(
            "/api/transactions/merchant/1",
            headers={"Authorization": f"Bearer {other_token}"},
        )
        assert other_response.status_code == 200
        assert other_response.json() == []