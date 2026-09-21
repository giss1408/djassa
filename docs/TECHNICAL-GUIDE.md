# Djassa Technical Guide

This document is the technical navigation page for the repository. It describes what each technical area owns and where to find the operational instructions.

## Current backend

The backend is a FastAPI service with:

- SQLAlchemy models and Alembic migrations.
- PostgreSQL as the target relational database.
- Redis and Celery for asynchronous work.
- JWT-based authentication in the current skeleton.
- Webhook signature verification and idempotency handling.
- Prometheus metrics and OpenTelemetry instrumentation.

The implementation is still a prototype. Authentication, resource authorization, financial workflows, and production configuration require further hardening before real financial use.

## Repository map

| Area | Location | Purpose |
|---|---|---|
| Backend API | [backend-api](../backend-api/) | FastAPI application, models, routes, workers, tests |
| Product concept | [PRODUCT-CONCEPT.md](PRODUCT-CONCEPT.md) | User problem, product boundary, value proposition |
| Business model | [BUSINESS-MODEL.md](BUSINESS-MODEL.md) | Customers, revenue, unit economics, boundaries |
| Partner strategy | [PARTNERS-AND-OUTREACH.md](PARTNERS-AND-OUTREACH.md) | Institutions, outreach, pilot questions |
| Product roadmap | [ROADMAP.md](ROADMAP.md) | Phases, dependencies, exit criteria |
| Architecture | [Architecture/README.md](../Architecture/README.md) | Canonical architecture index and deployment modes |
| Security | [Architecture/SECURITY.md](../Architecture/SECURITY.md) | Application and financial-security principles |
| Container security | [Architecture/security-architecture.md](../Architecture/security-architecture.md) | Compose/Kubernetes hardening |
| VPS test deployment | [VPS-TEST-SERVER.md](VPS-TEST-SERVER.md) | Test-server setup and automated deployment |
| Database migrations | [backend-api/MIGRATIONS.md](../backend-api/MIGRATIONS.md) | Schema changes, rollback, and deployment rules |
| Contributions | [CONTRIBUTING.md](../CONTRIBUTING.md) | Branches, tests, and security checklist |
| Contributor guidance | [skills](../skills/) | Implementation and writing guidance |
| Jenkins CI/CD | [Jenkinsfile](../Jenkinsfile) | Validation, image supply-chain checks, publishing, and gated deployment |

## Local development

From `backend-api`:

```bash
python3 -m venv .venv
. .venv/bin/activate
pip install -r requirements.txt
docker compose -f docker-compose.dev.yml up -d db redis
export DATABASE_URL=postgresql+asyncpg://djassa:djassa@127.0.0.1:5432/djassa
alembic -c alembic.ini upgrade head
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Run tests with:

```bash
pytest -q
```

Schema changes follow [MIGRATIONS.md](../backend-api/MIGRATIONS.md). Apply migrations explicitly before starting a new deployment.

Run the worker in a second terminal:

```bash
export CELERY_BROKER_URL=redis://127.0.0.1:6379/0
celery -A app.celery_app.celery_app worker --loglevel=info
```

## VPS test deployment

Use the automated deployment script, not the development server:

```bash
cd backend-api
./deploy-vps-test.sh
```

The script builds the image, creates test-only secrets, starts dependencies, applies migrations, starts the API and worker, and verifies health. See [VPS-TEST-SERVER.md](VPS-TEST-SERVER.md) for prerequisites and access controls.

## Configuration contract

Required production-like variables:

| Variable | Purpose |
|---|---|
| `DATABASE_URL` | PostgreSQL connection URL |
| `DJASSA_SECRET_KEY` | JWT signing key; never use a placeholder |
| `MOBILE_MONEY_SECRETS` | Comma-separated webhook signing keys |
| `CELERY_BROKER_URL` | Redis broker URL |

Do not use the demo credentials or placeholder secrets on an Internet-accessible server.

## Technical decision rules

- Use migrations for schema changes; do not rely on `create_all` for production rollout.
- Derive ownership from the authenticated identity, never from an untrusted request body.
- Protect every export and financial read with explicit authorization.
- Treat payment webhooks as untrusted input; verify signatures, timestamps, and idempotency.
- Keep PostgreSQL, Redis, metrics, and internal worker endpoints private.
- Add tests for unauthorized access and cross-user data isolation with every sensitive endpoint.

## Before production

The following remain mandatory work:

- Replace demo authentication with a real identity and user store.
- Implement role and resource authorization.
- Remove default secrets and fail closed at startup.
- Add refresh-token or session revocation strategy.
- Complete payment reconciliation and financial state transitions.
- Add backup and restore procedures.
- Enforce immutable image versions and blocking vulnerability scans.
- Review regulatory responsibilities with qualified local counsel and licensed partners.
