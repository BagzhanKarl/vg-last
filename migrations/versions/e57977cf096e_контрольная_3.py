"""Контрольная 3

Revision ID: e57977cf096e
Revises: 4eb7be59e89b
Create Date: 2025-01-10 16:47:44.415607

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'e57977cf096e'
down_revision = '4eb7be59e89b'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avatar', schema=None) as batch_op:
        batch_op.add_column(sa.Column('lang', sa.String(length=150), nullable=False))
        batch_op.add_column(sa.Column('temp', sa.Float(), nullable=False))

    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    with op.batch_alter_table('avatar', schema=None) as batch_op:
        batch_op.drop_column('temp')
        batch_op.drop_column('lang')

    # ### end Alembic commands ###
