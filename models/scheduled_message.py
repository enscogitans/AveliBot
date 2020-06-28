from sqlalchemy import Column, Integer, ForeignKey, TIMESTAMP, String

from .base import Base
from .chat import Chat


class ScheduledMessage(Base):  # type: ignore
    __tablename__ = "scheduled_messages"

    chat_id = Column(
        ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        primary_key=True
    )
    message_id = Column(Integer, primary_key=True)
    text = Column(String, nullable=False)
    deadline = Column(TIMESTAMP(timezone=True), nullable=False)
