"""Контрольная 2

Revision ID: 4eb7be59e89b
Revises: fddf674d8ee4
Create Date: 2025-01-10 15:58:06.510262

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4eb7be59e89b'
down_revision = 'fddf674d8ee4'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avatar', schema=None) as batch_op:
        batch_op.add_column(sa.Column('is_active', sa.Boolean(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avatar', schema=None) as batch_op:
        batch_op.drop_column('is_active')

    # ### end Alembic commands ###
