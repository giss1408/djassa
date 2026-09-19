This folder contains manifests and compose files to run Prometheus, Grafana, Alertmanager,
and common exporters for local development and Kubernetes.

Quick start (docker-compose):

```bash
cd monitoring
docker-compose -f docker-compose.monitoring.yml up -d
# Open Grafana: http://localhost:3000 (admin/admin)
# Prometheus: http://localhost:9090
# Alertmanager: http://localhost:9093
```

Provisioning notes:
- Grafana is pre-provisioned with Prometheus data source and dashboards for API/Redis/Postgres.
- Alertmanager is configured with a basic `critical` alert routing to console.
