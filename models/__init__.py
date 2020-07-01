from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from config import POSTGRES_URI
from .base import Base
# import all the models so that Alembic could see them
from .chat import Chat
from .chat_member import ChatMember
from .scheduled_message import ScheduledMessage
from .user import User
from .wolf_winner import WolfWinner

__all__ = ["db", "Base", "Chat", "ChatMember", "ScheduledMessage", "User", "WolfWinner"]

engine = create_engine(POSTGRES_URI)
Session = sessionmaker(bind=engine)
db = Session()
