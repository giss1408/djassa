from sqlalchemy import select
from sqlalchemy.ext.asyncio import AsyncSession
from datetime import datetime
from ..db import AsyncSessionLocal
from .. import models
from prometheus_client import Gauge, Counter

# Domain metrics
try:
    TONTINE_ACTIVE_CYCLES = Gauge('tontine_cycles_active', 'Active cycles', ['group'])
    TONTINE_CONTRIBUTIONS = Counter('tontine_contributions_total', 'Total contributions')
except Exception:
    # prometheus client may already be initialized in forked worker
    TONTINE_ACTIVE_CYCLES = None
    TONTINE_CONTRIBUTIONS = None

# Synchronous wrappers that can be called from Celery (which may run in a separate process)
# For testing we also expose async helpers.

def create_cycle_and_assign_payout_sync(group_id: int):
    # run an async function in event loop
    import asyncio
    return asyncio.run(create_cycle_and_assign_payout(group_id))

async def create_cycle_and_assign_payout(group_id: int):
    async with AsyncSessionLocal() as session:
        # get members ordered by joined_at
        res = await session.execute(select(models.TontineMember).where(models.TontineMember.group_id==group_id, models.TontineMember.active==True).order_by(models.TontineMember.joined_at))
        members = res.scalars().all()
        if not members:
            return None
        # find last payout
        res2 = await session.execute(select(models.TontineCycle).where(models.TontineCycle.group_id==group_id).order_by(models.TontineCycle.cycle_number.desc()).limit(1))
        last_cycle = res2.scalar_one_or_none()
        next_index = 0
        if last_cycle and last_cycle.payout_member_id:
            # map id to index
            ids = [m.id for m in members]
            if last_cycle.payout_member_id in ids:
                last_idx = ids.index(last_cycle.payout_member_id)
                next_index = (last_idx + 1) % len(members)
        payout_member = members[next_index]
        # create cycle
        cycle_number = (last_cycle.cycle_number + 1) if last_cycle else 1
        new_cycle = models.TontineCycle(group_id=group_id, cycle_number=cycle_number, start_at=datetime.utcnow(), status='open', payout_member_id=payout_member.id)
        session.add(new_cycle)
        await session.commit()
        await session.refresh(new_cycle)
        try:
            if TONTINE_ACTIVE_CYCLES:
                TONTINE_ACTIVE_CYCLES.labels(group=str(group_id)).inc()
        except Exception:
            pass
        return {'cycle_id': new_cycle.id, 'payout_member_id': payout_member.id}


def process_webhook_sync(external_id: str):
    import asyncio
    return asyncio.run(process_webhook(external_id))


async def process_webhook(external_id: str):
    async with AsyncSessionLocal() as session:
        # Simple placeholder: mark webhook event processed in logs
        res = await session.execute(select(models.WebhookEvent).where(models.WebhookEvent.external_id==external_id))
        event = res.scalar_one_or_none()
        if not event:
            return {'status': 'not_found'}
        # Business processing would occur here: reconcile, credit account, emit events
        # write processing log
        log = models.WebhookProcessingLog(external_id=external_id, status='processed')
        session.add(log)
        await session.commit()
        try:
            if TONTINE_CONTRIBUTIONS:
                TONTINE_CONTRIBUTIONS.inc()
        except Exception:
            pass
        return {'status': 'processed', 'external_id': external_id}


def close_due_cycles_sync():
    import asyncio
    return asyncio.run(close_due_cycles())

async def close_due_cycles():
    async with AsyncSessionLocal() as session:
        from sqlalchemy import and_
        now = datetime.utcnow()
        res = await session.execute(select(models.TontineCycle).where(models.TontineCycle.end_at != None, models.TontineCycle.end_at <= now, models.TontineCycle.status=='open'))
        cycles = res.scalars().all()
        closed = []
        for c in cycles:
            c.status = 'closed'
            session.add(c)
            closed.append(c.id)
        await session.commit()
        try:
            if TONTINE_ACTIVE_CYCLES:
                # recompute per-group active cycles
                for gid in set([c.group_id for c in cycles]):
                    res = await session.execute(select(models.TontineCycle).where(models.TontineCycle.group_id==gid, models.TontineCycle.status=='open'))
                    count = len(res.scalars().all())
                    TONTINE_ACTIVE_CYCLES.labels(group=str(gid)).set(count)
        except Exception:
            pass
        return {'closed_cycles': closed}
