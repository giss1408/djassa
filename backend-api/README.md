# djassa — backend-api (skeleton)

Minimal FastAPI skeleton for the `djassa` backend.

Run locally:

```bash
python -m pip install -r requirements.txt
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run with Postgres (development):

```bash
docker compose -f docker-compose.dev.yml up -d db
export DATABASE_URL=postgresql+asyncpg://djassa:djassa@127.0.0.1:5432/djassa
alembic -c alembic.ini upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Docker build (example):

```bash
docker build -t registry.example.com/djassa/api:dev .
```

Endpoints:
- `GET /health` — health check
- `GET /ready` — readiness
- `POST /api/payments` — create payment (example)
Additional endpoints:
- `POST /api/transactions` — record a merchant transaction (requires auth)
- `GET /api/transactions/merchant/{merchant_id}` — list merchant transactions (requires auth)
- `POST /api/consents` — create consent for export (requires auth)
- `GET /api/export/merchant/{merchant_id}` — export merchant transactions as CSV (requires consent)
