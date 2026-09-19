from prometheus_client import Counter, Histogram, Gauge
from prometheus_client import generate_latest, CONTENT_TYPE_LATEST
from fastapi import Request
import time

# Request metrics
HTTP_REQUEST_COUNT = Counter(
    'http_requests_total', 'Total HTTP requests', ['method', 'path', 'status']
)

HTTP_REQUEST_LATENCY = Histogram(
    'http_request_duration_seconds', 'HTTP request duration', ['method', 'path']
)

# DB metrics
DB_CONNECTIONS = Gauge('db_active_connections', 'Active DB connections')

# SQL query latency histogram
DB_QUERY_LATENCY = Histogram('db_query_duration_seconds', 'DB query duration', ['query'])

# Celery metrics
CELERY_TASKS_TOTAL = Counter('celery_tasks_total', 'Total Celery tasks', ['task', 'status'])

def record_request(method, path, status, duration):
    HTTP_REQUEST_COUNT.labels(method=method, path=path, status=str(status)).inc()
    HTTP_REQUEST_LATENCY.labels(method=method, path=path).observe(duration)


def record_db_query(query, duration):
    try:
        DB_QUERY_LATENCY.labels(query=query[:100]).observe(duration)
    except Exception:
        pass

def metrics_endpoint():
    data = generate_latest()
    return CONTENT_TYPE_LATEST, data
