import asyncio
import typing as tp

from aiogram import types
from aiogram.dispatcher.middlewares import BaseMiddleware

from models.chat import Chat
from models.chat_member import ChatMember
from models.user import User


class ACLMiddleware(BaseMiddleware):  # type: ignore
    @staticmethod
    async def add_chat(chat: types.Chat) -> Chat:
        db_chat = await Chat.get(chat.id)
        if db_chat is None:
            db_chat = await Chat.create(id=chat.id)
        return db_chat

    @staticmethod
    async def add_user(user: types.User) -> User:
        db_user = await User.get(user.id)
        if db_user is None:
            db_user = await User.create(id=user.id)
        return db_user

    @staticmethod
    async def add_member(chat: types.Chat, user: types.User, has_left: bool) -> None:
        await ACLMiddleware.add_chat(chat)
        await ACLMiddleware.add_user(user)
        member = await ChatMember.get({"chat_id": chat.id, "user_id": user.id})
        if member is None:
            return await ChatMember.create(chat_id=chat.id, user_id=user.id, has_left=has_left)
        return await member.update(has_left=has_left).apply()

    async def on_pre_process_message(self, message: types.Message, data: tp.Dict[tp.Any, tp.Any]) -> None:
        if not types.ChatType.is_group_or_super_group(message):
            return

        if not message.from_user.is_bot:
            await self.add_member(message.chat, message.from_user, has_left=False)

        if message.content_type == types.ContentType.LEFT_CHAT_MEMBER:  # noqa: E721
            await self.add_member(message.chat, message.left_chat_member, has_left=True)
        elif message.content_type == types.ContentType.NEW_CHAT_MEMBERS:  # noqa: E721
            new_members = [mem for mem in message.new_chat_members if not mem.is_bot]
            tasks = [self.add_member(message.chat, mem, has_left=False) for mem in new_members]
            await asyncio.gather(*tasks)
