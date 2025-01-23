"""Migration 3

Revision ID: fb9c8a6a43f5
Revises: 5aab38d5d987
Create Date: 2025-01-24 04:12:01.422203

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'fb9c8a6a43f5'
down_revision = '5aab38d5d987'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('user_logs',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('event_type', sa.String(length=50), nullable=True),
    sa.Column('data', sa.JSON(), nullable=True),
    sa.Column('status', sa.String(length=50), nullable=True),
    sa.Column('error_message', sa.Text(), nullable=True),
    sa.Column('created_at', sa.DateTime(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('user_logs')
    # ### end Alembic commands ###
