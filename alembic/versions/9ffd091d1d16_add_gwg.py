"""Add GwG

Revision ID: 9ffd091d1d16
Revises:
Create Date: 2016-11-16 22:28:00.569382

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '9ffd091d1d16'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invoices', sa.Column('gwg', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    pass
