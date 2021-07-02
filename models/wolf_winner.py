from sqlalchemy import BigInteger, Column, Date, ForeignKey, Integer

from .base import Base
from .chat import Chat
from .user import User


class WolfWinner(Base):
    __tablename__ = "wolf_winners"

    chat_id = Column(
        BigInteger,
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    date = Column(Date, primary_key=True)
    user_id = Column(
        Integer,
        ForeignKey(f"{User.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False
    )
