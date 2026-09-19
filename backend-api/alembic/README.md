Alembic migrations live here. Run:

```bash
alembic -c alembic.ini revision --autogenerate -m "init"
alembic -c alembic.ini upgrade head
```

Ensure `DATABASE_URL` env var points to the target DB.
