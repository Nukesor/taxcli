"""empty message

Revision ID: 97519c3acc64
Revises: 9ffd091d1d16
Create Date: 2016-11-17 00:36:18.728149

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '97519c3acc64'
down_revision = '9ffd091d1d16'
branch_labels = None
depends_on = None


def upgrade():
    op.create_check_constraint(
        'invoices_afa_gwg_check', 'invoices',
        'afa is not null and gwg is false or '
        'afa is null and gwg is true or '
        'afa is null and gwg is false')


def downgrade():
    pass
