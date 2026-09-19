"""add tontine tables

Revision ID: 0002_tontine
Revises: 0001_initial
Create Date: 2026-09-19 00:00:00.000001
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0002_tontine'
down_revision = '0001_initial'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'tontine_groups',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('organizer_id', sa.String(length=128), nullable=False),
        sa.Column('contribution_amount', sa.Numeric(), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('frequency', sa.String(length=32), nullable=False),
        sa.Column('max_members', sa.Integer(), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'tontine_members',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey('tontine_groups.id'), nullable=False),
        sa.Column('user_id', sa.String(length=128), nullable=False),
        sa.Column('joined_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('is_admin', sa.Boolean(), nullable=True),
        sa.Column('active', sa.Boolean(), nullable=True),
    )

    op.create_table(
        'tontine_cycles',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey('tontine_groups.id'), nullable=False),
        sa.Column('cycle_number', sa.Integer(), nullable=False),
        sa.Column('start_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('end_at', sa.DateTime(timezone=True), nullable=True),
        sa.Column('payout_member_id', sa.Integer(), sa.ForeignKey('tontine_members.id'), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
        sa.Column('created_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'tontine_contributions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('group_id', sa.Integer(), sa.ForeignKey('tontine_groups.id'), nullable=False),
        sa.Column('cycle_id', sa.Integer(), sa.ForeignKey('tontine_cycles.id'), nullable=True),
        sa.Column('member_id', sa.Integer(), sa.ForeignKey('tontine_members.id'), nullable=False),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('paid_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
        sa.Column('payment_reference', sa.String(length=255), nullable=True),
        sa.Column('status', sa.String(length=32), nullable=False),
    )


def downgrade():
    op.drop_table('tontine_contributions')
    op.drop_table('tontine_cycles')
    op.drop_table('tontine_members')
    op.drop_table('tontine_groups')
