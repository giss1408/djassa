import pytest
from app.services import tontine as tontine_service
from app.db import AsyncSessionLocal
from app import models
import asyncio


@pytest.mark.asyncio
async def test_create_cycle_round_robin():
    async with AsyncSessionLocal() as session:
        # create group
        group = models.TontineGroup(name='RR Group', organizer_id='org', contribution_amount=100, currency='XOF')
        session.add(group)
        await session.commit()
        await session.refresh(group)
        gid = group.id

        # add three members
        m1 = models.TontineMember(group_id=gid, user_id='u1')
        m2 = models.TontineMember(group_id=gid, user_id='u2')
        m3 = models.TontineMember(group_id=gid, user_id='u3')
        session.add_all([m1, m2, m3])
        await session.commit()

        # create first cycle
        result1 = await tontine_service.create_cycle_and_assign_payout(gid)
        assert result1 and 'payout_member_id' in result1
        first = result1['payout_member_id']

        # create second cycle
        result2 = await tontine_service.create_cycle_and_assign_payout(gid)
        assert result2 and result2['payout_member_id'] != first

        # create third cycle
        result3 = await tontine_service.create_cycle_and_assign_payout(gid)
        # after three cycles, rotation should wrap back to first
        assert result3 and result3['payout_member_id'] != result2['payout_member_id']
