"""create matches table

Revision ID: 8f4c2a1d6b90
Revises: 2e4e9d5dbcdc
Create Date: 2026-09-22 19:05:00.000000
"""

from alembic import op
import sqlalchemy as sa
from sqlalchemy.dialects import postgresql


revision = "8f4c2a1d6b90"
down_revision = "2e4e9d5dbcdc"
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        "matches",
        sa.Column("id", postgresql.UUID(as_uuid=True), nullable=False),
        sa.Column("team_a", sa.String(), nullable=False),
        sa.Column("team_b", sa.String(), nullable=False),
        sa.Column("venue", sa.String(), nullable=False),
        sa.Column("status", sa.String(), nullable=False, server_default="LIVE"),
        sa.Column("created_at", sa.DateTime(), server_default=sa.func.now()),
        sa.PrimaryKeyConstraint("id"),
    )


def downgrade():
    op.drop_table("matches")
