import asyncio
import logging
from sqlalchemy import select
from .db import AsyncSessionLocal
from . import models

logger = logging.getLogger("tontine.tasks")


async def notify_reminders():
    # Placeholder: scan open cycles and send reminder (integrate with SMS/Push/email)
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(models.TontineCycle).where(models.TontineCycle.status == "open"))
        cycles = res.scalars().all()
        for c in cycles:
            logger.debug(f"Reminder: cycle {c.id} for group {c.group_id}")


async def close_due_cycles():
    # Placeholder: find cycles past end_at and mark closed
    async with AsyncSessionLocal() as session:
        res = await session.execute(select(models.TontineCycle).where(models.TontineCycle.end_at != None))
        cycles = res.scalars().all()
        for c in cycles:
            # simplistic: if end_at passed, mark closed
            if c.end_at:
                # note: real code must compare timezone-aware datetimes
                logger.debug(f"Would close cycle {c.id}")


async def background_worker(interval_seconds: int = 60):
    while True:
        try:
            await notify_reminders()
            await close_due_cycles()
        except Exception as e:
            logger.exception("Background worker error")
        await asyncio.sleep(interval_seconds)
