from sqlalchemy import BigInteger, Boolean, Column, ForeignKey, Integer

from .base import Base
from .chat import Chat
from .user import User


class ChatMember(Base):
    __tablename__ = "chat_members"

    chat_id = Column(
        BigInteger,
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    user_id = Column(
        Integer,
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    has_left = Column(Boolean)
    play_wolf_game = Column(Boolean, default=True, nullable=False)
