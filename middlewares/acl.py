import typing as tp

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models import db, Chat, ChatMember, User


class ACLMiddleware(BaseMiddleware):  # type: ignore
    @staticmethod
    def add_chat(chat: types.Chat) -> Chat:
        db_chat = db.query(Chat).get(chat.id)
        if db_chat is None:
            db_chat = Chat(id=chat.id)
            db.add(db_chat)
            db.commit()
        return db_chat

    @staticmethod
    def add_user(user: types.User) -> User:
        db_user = db.query(User).get(user.id)
        if db_user is None:
            db_user = User(id=user.id)
            db.add(db_user)
            db.commit()
        return db_user

    @staticmethod
    def add_member(chat: types.Chat, user: types.User, has_left: bool) -> None:
        ACLMiddleware.add_chat(chat)
        ACLMiddleware.add_user(user)
        member = db.query(ChatMember).get({"chat_id": chat.id, "user_id": user.id})
        if member is not None:
            member.has_left = has_left
        else:
            member = ChatMember(chat_id=chat.id, user_id=user.id, has_left=has_left)
            db.add(member)
        db.commit()
        return member

    async def on_pre_process_message(self, message: types.Message, data: tp.Dict[tp.Any, tp.Any]) -> None:
        if not types.ChatType.is_group_or_super_group(message):
            return

        if not message.from_user.is_bot:
            self.add_member(message.chat, message.from_user, has_left=False)

        if message.content_type == types.ContentType.LEFT_CHAT_MEMBER:  # noqa: E721
            self.add_member(message.chat, message.left_chat_member, has_left=True)
        elif message.content_type == types.ContentType.NEW_CHAT_MEMBERS:  # noqa: E721
            for mem in message.new_chat_members:
                if not mem.is_bot:
                    self.add_member(message.chat, mem, has_left=False)
