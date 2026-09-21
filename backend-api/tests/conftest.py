import os
import asyncio
import pytest


# Keep test defaults explicit while production startup fails closed on missing secrets.
os.environ.setdefault("DJASSA_SECRET_KEY", "test-only-jwt-secret")
os.environ.setdefault("MOBILE_MONEY_SECRETS", "dev-secret")
os.environ.setdefault("DATABASE_URL", "sqlite+aiosqlite:////tmp/djassa-test.db")


@pytest.fixture(scope="session", autouse=True)
def initialize_database():
	from app.db import engine, Base

	async def create_tables():
		async with engine.begin() as connection:
			await connection.run_sync(Base.metadata.create_all)

	asyncio.run(create_tables())
	yield

	async def dispose_engine():
		await engine.dispose()

	asyncio.run(dispose_engine())