"""create users table

Revision ID: 2e4e9d5dbcdc
Revises: 
Create Date: 2026-01-19 11:18:17.306190
"""

from alembic import op
import sqlalchemy as sa

# revision identifiers, used by Alembic.
revision = '2e4e9d5dbcdc'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.create_table(
        'users',
        sa.Column('id', sa.Integer, primary_key=True),
        sa.Column('email', sa.String(255), nullable=False, unique=True),
        sa.Column('hashed_password', sa.String(255), nullable=False),
        sa.Column('role', sa.String(50), nullable=False),
        sa.Column('created_at', sa.DateTime(), nullable=True)
    )


def downgrade():
    op.drop_table('users')
