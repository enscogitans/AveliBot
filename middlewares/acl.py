import typing as tp

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware
from sqlalchemy import orm

from models import Chat, ChatMember, User


class ACLMiddleware(BaseMiddleware):  # type: ignore
    def __init__(self, session: orm.Session):
        super().__init__()
        self.session = session

    def add_chat(self, chat: types.Chat) -> Chat:
        db_chat = self.session.query(Chat).get(chat.id)
        if db_chat is None:
            db_chat = Chat(id=chat.id)
            self.session.add(db_chat)
            self.session.commit()
        return db_chat

    def add_user(self, user: types.User) -> User:
        db_user = self.session.query(User).get(user.id)
        if db_user is None:
            db_user = User(id=user.id)
            self.session.add(db_user)
            self.session.commit()
        return db_user

    def add_member(self, chat: types.Chat, user: types.User, has_left: bool) -> ChatMember:
        self.add_chat(chat)
        self.add_user(user)
        member = self.session.query(ChatMember).get({"chat_id": chat.id, "user_id": user.id})
        if member is not None:
            member.has_left = has_left
        else:
            member = ChatMember(chat_id=chat.id, user_id=user.id, has_left=has_left)
            self.session.add(member)
        self.session.commit()
        return member

    async def on_pre_process_message(self, message: types.Message, data: tp.Dict[tp.Any, tp.Any]) -> None:
        if message.chat.type not in (types.ChatType.GROUP, types.ChatType.SUPERGROUP):
            return

        if not message.from_user.is_bot:
            self.add_member(message.chat, message.from_user, has_left=False)

        if message.content_type == types.ContentType.LEFT_CHAT_MEMBER:  # noqa: E721
            self.add_member(message.chat, message.left_chat_member, has_left=True)
        elif message.content_type == types.ContentType.NEW_CHAT_MEMBERS:  # noqa: E721
            for mem in message.new_chat_members:
                if not mem.is_bot:
                    self.add_member(message.chat, mem, has_left=False)
