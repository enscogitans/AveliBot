from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_URI
from .base import Base
# import all the models so that Alembic could see them
from .chat import Chat
from .chat_member import ChatMember
from .user import User

__all__ = ["db", "Base", "Chat", "ChatMember", "User"]

engine = create_engine(POSTGRES_URI)
Session = sessionmaker(bind=engine)
db = Session()
