from .db import db
from .chat import ChatRelatedModel
from .user import UserRelatedModel


class ChatMember(ChatRelatedModel, UserRelatedModel):
    __tablename__ = "chat_members"

    has_left = db.Column(db.Boolean)

    _pk = db.PrimaryKeyConstraint("chat_id", "user_id", name="chat_member_pkey")
