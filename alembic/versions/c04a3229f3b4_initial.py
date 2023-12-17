"""initial

Revision ID: c04a3229f3b4
Revises: 
Create Date: 2023-12-17 21:38:08.245822

"""
from typing import Sequence, Union

from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision: str = 'c04a3229f3b4'
down_revision: Union[str, None] = None
branch_labels: Union[str, Sequence[str], None] = None
depends_on: Union[str, Sequence[str], None] = None


def upgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('users',
    sa.Column('telegram_id', sa.Integer(), nullable=True),
    sa.Column('chat_id', sa.Integer(), nullable=False),
    sa.Column('meta', sa.String(length=255), nullable=False),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_table('notifications',
    sa.Column('start_date', sa.DateTime(), nullable=False),
    sa.Column('notification_hour', sa.Integer(), nullable=False),
    sa.Column('notification_minute', sa.Integer(), nullable=False),
    sa.Column('drug_name', sa.String(length=255), nullable=False),
    sa.Column('drug_type', sa.String(length=255), nullable=False),
    sa.Column('amount', sa.Integer(), nullable=False),
    sa.Column('end_date', sa.DateTime(), nullable=False),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.Column('id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['user_id'], ['users.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    # ### end Alembic commands ###


def downgrade() -> None:
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('notifications')
    op.drop_table('users')
    # ### end Alembic commands ###
