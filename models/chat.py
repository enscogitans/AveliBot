from sqlalchemy import Column, BigInteger, String
from sqlalchemy.orm import relationship

from .base import Base


class Chat(Base):  # type: ignore
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    timezone = Column(String, default="Europe/Moscow")

    members = relationship("ChatMember")
