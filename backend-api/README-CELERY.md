Celery worker and Redis (dev)

1) Start Redis (we provide a redis service in `docker-compose.dev.yml`):

```bash
docker compose -f docker-compose.dev.yml up -d redis
```

2) Export broker URL and start worker:

```bash
export CELERY_BROKER_URL=redis://127.0.0.1:6379/0
export CELERY_RESULT_BACKEND=redis://127.0.0.1:6379/0
celery -A app.celery_app.celery_app worker --loglevel=info
```

3) Periodic tasks: use `celery beat` or a Kubernetes CronJob for scheduled jobs.
