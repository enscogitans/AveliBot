from sqlalchemy import BigInteger, Column, ForeignKey, Integer, String, TIMESTAMP

from .base import Base
from .chat import Chat


class ScheduledMessage(Base):
    __tablename__ = "scheduled_messages"

    chat_id = Column(
        BigInteger,
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    message_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
