from sqlalchemy import Column, Date, ForeignKey

from .base import Base
from .chat import Chat
from .user import User


class WolfWinner(Base):  # type: ignore
    __tablename__ = "wolf_winners"

    chat_id = Column(
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    date = Column(Date, primary_key=True)
    user_id = Column(
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
