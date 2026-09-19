# djassa backend — HOWTO

This document explains how to set up and run the `djassa` backend locally and in CI. Follow the steps below. Do NOT commit any credentials — keep them in environment variables or an `.env` file (listed in `.gitignore`).

## 1) Prepare a Python virtual environment

```bash
cd backend-api
python3 -m venv .venv
source .venv/bin/activate
python -m pip install --upgrade pip
pip install -r requirements.txt
```

## 2) Running with local Postgres (recommended)

Start Postgres using the provided `docker-compose.dev.yml`:

```bash
docker compose -f docker-compose.dev.yml up -d db
```

Set the `DATABASE_URL` env var for the app and Alembic:

```bash
export DATABASE_URL=postgresql+asyncpg://djassa:djassa@127.0.0.1:5432/djassa
```

Apply database migrations (Alembic):

```bash
alembic -c alembic.ini upgrade head
```

Run the development server:

```bash
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

Open http://localhost:8000/docs for the OpenAPI docs.

## 3) Running without Postgres (SQLite fallback)

By default the app falls back to `sqlite+aiosqlite:///./test.db` if `DATABASE_URL` is not set. This is convenient for quick local experiments but not recommended for CI or production.

To run with the fallback DB:

```bash
unset DATABASE_URL
uvicorn app.main:app --reload
```

## 4) Running tests

Use the virtualenv and ensure dependencies are installed. For the fastest parity with CI, start the local Postgres service first and set `DATABASE_URL` as above, then run:

```bash
pytest -q
```

If you prefer to run tests against SQLite (quick run), unset `DATABASE_URL` and run `pytest -q` — note that some integration behaviours may differ.

## 5) Running the app in Docker (build and run)

Build the image:

```bash
docker build -t registry.example.com/djassa/api:dev .
```

Run with environment variables (example):

```bash
docker run -e DATABASE_URL=postgresql+asyncpg://djassa:djassa@db:5432/djassa -p 8000:8000 registry.example.com/djassa/api:dev
```

## 6) CI notes

- GitHub Actions workflow runs the SBOM and Trivy scans, starts a Postgres service, waits for it to be ready, runs Alembic migrations, and then runs `pytest`.
- Store registry credentials and any production database credentials as GitHub Secrets (e.g. `REGISTRY_URL`, `REGISTRY_USERNAME`, `REGISTRY_PASSWORD`).

### Add Trivy image scan to GitHub Actions

Add a workflow step that runs Trivy against the built image and fails if critical vulnerabilities are found. Example job snippet:

```yaml
- name: Scan image with Trivy
	uses: aquasecurity/trivy-action@v0.3.0
	with:
		image-ref: registry.example.com/djassa/api:dev
		exit-code: '1'
		severity: CRITICAL
		format: 'table'
```

## 7) Security & secrets

- Do not commit `.env` files or credentials. Use environment variables or a secrets manager (External Secrets in Kubernetes is configured in `Architecture/k8s/external-secret-example.yaml`).
- The file `.gitignore` already excludes `.env`, `.venv`, `infra/secrets/` and common credential file extensions.

## 8) Useful commands summary

```bash
# start postgres locally
docker compose -f docker-compose.dev.yml up -d db

# run migrations
export DATABASE_URL=postgresql+asyncpg://djassa:djassa@127.0.0.1:5432/djassa
alembic -c alembic.ini upgrade head

# run server
uvicorn app.main:app --reload

# run tests
pytest -q
```

If you want, I can add a `Makefile` or convenience `scripts/` wrappers for these commands. Which would you prefer? 
