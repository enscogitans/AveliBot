from .db import db


class Chat(db.Model):  # type: ignore
    __tablename__ = "chats"

    id = db.Column(db.BigInteger, primary_key=True)
    timezone = db.Column(db.String, default="+0300")


class ChatRelatedModel(db.Model):  # type: ignore
    chat_id = db.Column(
        db.ForeignKey(f"{Chat.__tablename__}.id", ondelete="CASCADE", onupdate="CASCADE"),
        nullable=False,
    )
