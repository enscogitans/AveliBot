"""add scheduled messages

Revision ID: 668fbf83f0ce
Revises: fc8a3770e288
Create Date: 2020-06-28 01:44:29.755019

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '668fbf83f0ce'
down_revision = 'fc8a3770e288'
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('scheduled_messages',
    sa.Column('chat_id', sa.BigInteger(), nullable=False),
    sa.Column('message_id', sa.Integer(), nullable=False),
    sa.Column('text', sa.String(), nullable=False),
    sa.Column('deadline', sa.TIMESTAMP(timezone=True), nullable=False),
    sa.ForeignKeyConstraint(['chat_id'], ['chats.id'], onupdate='CASCADE', ondelete='CASCADE'),
    sa.PrimaryKeyConstraint('chat_id', 'message_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('scheduled_messages')
    # ### end Alembic commands ###
