"""initial tables

Revision ID: 0001_initial
Revises: 
Create Date: 2026-09-19 00:00:00.000000
"""
from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '0001_initial'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'merchants',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('name', sa.String(length=255), nullable=False),
        sa.Column('external_id', sa.String(length=255), nullable=True),
        sa.Column('description', sa.Text(), nullable=True),
    )

    op.create_table(
        'transactions',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('merchant_id', sa.Integer(), sa.ForeignKey('merchants.id'), nullable=False, index=True),
        sa.Column('user_id', sa.String(length=128), nullable=True),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('type', sa.String(length=32), nullable=False),
        sa.Column('timestamp', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )

    op.create_table(
        'payments',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('amount', sa.Numeric(), nullable=False),
        sa.Column('currency', sa.String(length=8), nullable=False),
        sa.Column('recipient_id', sa.String(length=128), nullable=False),
    )

    op.create_table(
        'consents',
        sa.Column('id', sa.Integer(), primary_key=True),
        sa.Column('user_id', sa.String(length=128), nullable=False),
        sa.Column('merchant_id', sa.Integer(), sa.ForeignKey('merchants.id'), nullable=False),
        sa.Column('scope', sa.String(length=255), nullable=False),
        sa.Column('granted_at', sa.DateTime(timezone=True), server_default=sa.func.now()),
    )


def downgrade():
    op.drop_table('consents')
    op.drop_table('payments')
    op.drop_table('transactions')
    op.drop_table('merchants')
