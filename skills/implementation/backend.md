# Skill: Implementation — Backend

Purpose: implement, test, and document backend services for `djassa` with an emphasis on clarity, security, and reproducibility.

When to use:
- Building GraphQL APIs, authentication, data persistence, and background jobs.

Recommended stack guidance (suggested, not prescriptive):
- Language: `Python` (FastAPI) or `Node.js` (Express / NestJS).
- Database: `PostgreSQL` for relational data; include migrations via `alembic` or `knex`.
- Auth: JWT with refresh tokens or OAuth2 where appropriate.
- Testing: unit tests with `pytest` or `jest`, and integration tests using a test database or Docker Testcontainers.

Key deliverables:
- Minimal runnable service with `README` and exact run commands.
- OpenAPI/Swagger contract for each API surface.
- Database schema and migration files.
- Tests demonstrating main flows and CI configuration snippet.

Prompt patterns:
- Task: "Implement endpoint `POST /api/payments` that validates input, writes to `payments` table, and returns created resource. Include request/response schema, tests, and migration." 

Contributor notes:
- Keep endpoints small and well-documented. Add example curl commands in the `README`.
- Prefer typed DTOs and input validation.
