"""empty message

Revision ID: c45d12536d7e
Revises: 5984edc38502
Create Date: 2017-03-31 01:42:55.278891

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'c45d12536d7e'
down_revision = '5984edc38502'
branch_labels = None
depends_on = None


def upgrade():
    op.add_column('invoices', sa.Column('pooling', sa.Boolean(), nullable=False, server_default='false'))


def downgrade():
    pass
