from fastapi import FastAPI
from .api import payments, auth, transactions, export, tontine, webhooks
from .db import engine, Base
from . import tasks
from starlette.middleware import Middleware
from slowapi.middleware import SlowAPIMiddleware
from fastapi.middleware.cors import CORSMiddleware
from starlette.middleware.base import BaseHTTPMiddleware
from .rate_limiter import limiter
from prometheus_client import start_http_server
from .metrics import record_request
import time

# Middleware stack
middleware = [
    Middleware(SlowAPIMiddleware),
    Middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])
]


@app.on_event("startup")
async def startup():
    # Create DB tables in the skeleton environment (sqlite default)
    async with engine.begin() as conn:
        await conn.run_sync(Base.metadata.create_all)

app = FastAPI(title="djassa API", middleware=middleware)

# Start Prometheus metrics server for local development
try:
    start_http_server(8001)
except Exception:
    pass

# security headers middleware
class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    async def dispatch(self, request, call_next):
        response = await call_next(request)
        response.headers["Strict-Transport-Security"] = "max-age=63072000; includeSubDomains; preload"
        response.headers["X-Content-Type-Options"] = "nosniff"
        response.headers["X-Frame-Options"] = "DENY"
        response.headers["Referrer-Policy"] = "no-referrer"
        response.headers["Permissions-Policy"] = "geolocation=()"
        return response

app.add_middleware(SecurityHeadersMiddleware)
app.state.limiter = limiter


@app.middleware("http")
async def prometheus_middleware(request: Request, call_next):
    start = time.time()
    response = await call_next(request)
    duration = time.time() - start
    # normalize path for metrics
    path = request.url.path
    record_request(request.method, path, response.status_code, duration)
    return response

app.include_router(auth.router, prefix="/api")
app.include_router(payments.router, prefix="/api")
app.include_router(transactions.router, prefix="/api")
app.include_router(export.router, prefix="/api")
app.include_router(tontine.router, prefix="/api")
app.include_router(webhooks.router)

# Expose /metrics endpoint for Prometheus to scrape (compose local)
from fastapi.responses import Response
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST


@app.get("/metrics")
def metrics():
    data = generate_latest()
    return Response(content=data, media_type=CONTENT_TYPE_LATEST)


@app.on_event("startup")
async def _start_background_worker():
    import asyncio
    # start the background worker loop (non-blocking)
    asyncio.create_task(tasks.background_worker())


@app.get("/health")
async def health():
    return {"status": "ok"}


@app.get("/ready")
async def ready():
    return {"ready": True}
