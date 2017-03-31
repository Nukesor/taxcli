"""Update invoice check constraint

Revision ID: 49e1c8c65f59
Revises: c45d12536d7e
Create Date: 2017-03-31 02:09:55.488859

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '49e1c8c65f59'
down_revision = 'c45d12536d7e'
branch_labels = None
depends_on = None


def upgrade():
    op.drop_constraint('invoices_afa_gwg_check', 'invoices')
    op.create_check_constraint(
        'invoices_afa_gwg_check', 'invoices',
        'pooling is TRUE and gwg is FALSE and afa is NULL or '
        'pooling is FALSE and afa is not NULL and gwg is FALSE or '
        'pooling is FALSE and afa is NULL and gwg is TRUE or '
        'pooling is FALSE and afa is NULL and gwg is FALSE')
    pass


def downgrade():
    pass
