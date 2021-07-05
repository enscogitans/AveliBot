import asyncio
import functools
import logging

from aiogram import Dispatcher, types
from aiogram.dispatcher.filters import Command, Regexp
from sqlalchemy import orm

from src.models import Chat
from src import utils


async def tag_all(session: orm.Session, message: types.Message) -> None:
    chat = message.chat
    db_chat = session.query(Chat).get(chat.id)
    if db_chat is None:
        logging.error(f"Chat {chat.id} not found in database")
        return
    known_members = [mem for mem in db_chat.members if not mem.has_left]  # type: ignore

    tasks = [chat.get_member(mem.user_id) for mem in known_members]
    members = await asyncio.gather(*tasks)
    tags = [utils.get_mention(mem.user) for mem in members]

    if tags:
        await message.answer(", ".join(tags), parse_mode="HTML")
    else:
        logging.error(f"No users found in chat {chat.id}")


def register(dp: Dispatcher, session: orm.Session) -> None:
    dp.register_message_handler(functools.partial(tag_all, session),
                                Command(["all"]) | Regexp(r"\B@all\b"),
                                is_user=True, is_group_or_supergroup=True)
