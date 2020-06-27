from sqlalchemy import Column, Boolean, ForeignKey

from .base import Base
from .chat import Chat
from .user import User


class ChatMember(Base):  # type: ignore
    __tablename__ = "chat_members"

    chat_id = Column(
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    user_id = Column(
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    has_left = Column(Boolean)
