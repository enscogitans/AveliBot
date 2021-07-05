"""add wolf game

Revision ID: bff61ca896f3
Revises: 668fbf83f0ce
Create Date: 2020-07-01 22:43:53.129150

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
from sqlalchemy import orm

import src.models

revision = 'bff61ca896f3'
down_revision = '668fbf83f0ce'
branch_labels = None
depends_on = None


def upgrade():
    op.create_table('wolf_winners',
        sa.Column('chat_id', sa.BigInteger(), nullable=False),
        sa.Column('date', sa.Date(), nullable=False),
        sa.Column('user_id', sa.Integer(), nullable=False),
        sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.ForeignKeyConstraint(['user_id'], ['users.id'], onupdate='CASCADE', ondelete='CASCADE'),
        sa.PrimaryKeyConstraint('chat_id', 'date')
    )
    sa.Table()

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    for chat in session.query(src.models.Chat):
        if chat.timezone == '+0300':
            chat.timezone = 'Europe/Moscow'
    session.commit()


def downgrade():
    op.drop_table('wolf_winners')

    bind = op.get_bind()
    session = orm.Session(bind=bind)
    for chat in session.query(src.models.Chat):
        if chat.timezone == 'Europe/Moscow':
            chat.timezone = '+0300'
    session.commit()
