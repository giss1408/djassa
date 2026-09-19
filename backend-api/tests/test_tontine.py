import pytest
from httpx import AsyncClient
from app.main import app


@pytest.mark.asyncio
async def test_tontine_flow():
    async with AsyncClient(app=app, base_url="http://test") as ac:
        token_resp = await ac.post("/api/token", data={"username": "demo", "password": "demo123"})
        assert token_resp.status_code == 200
        token = token_resp.json()["access_token"]

        headers = {"Authorization": f"Bearer {token}"}

        # create group
        r = await ac.post(
            "/api/tontines",
            json={"name": "Test Group", "organizer_id": "org1", "contribution_amount": 100.0},
            headers=headers,
        )
        assert r.status_code == 200
        group = r.json()
        gid = group["id"]

        # join
        r2 = await ac.post(f"/api/tontines/{gid}/join", json={"user_id": "user1"}, headers=headers)
        assert r2.status_code == 200

        # contribute
        r3 = await ac.post(f"/api/tontines/{gid}/contribute", json={"user_id": "user1", "amount": 100.0}, headers=headers)
        assert r3.status_code == 200

        # list cycles (empty initially)
        r4 = await ac.get(f"/api/tontines/{gid}/cycles")
        assert r4.status_code == 200

        # export CSV
        r5 = await ac.get(f"/api/tontines/{gid}/export")
        assert r5.status_code == 200
        assert "text/csv" in r5.headers.get("content-type", "")
