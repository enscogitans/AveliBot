import typing

from sqlalchemy import BigInteger, Column, String
from sqlalchemy.orm import relationship

from .base import Base
if typing.TYPE_CHECKING:  # Required by mypy(sqlalchemy-stubs) to check relationship
    from .chat_member import ChatMember  # noqa: F401


class Chat(Base):
    __tablename__ = "chats"

    id = Column(BigInteger, primary_key=True)
    timezone = Column(String, default="Europe/Moscow")

    members = relationship("ChatMember")
