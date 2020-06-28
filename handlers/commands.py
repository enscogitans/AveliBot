import asyncio
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Regexp

from models import db, Chat
from utils import utils


async def tag_all(message: types.Message) -> None:
    chat = message.chat
    db_chat = db.query(Chat).get(chat.id)
    if db_chat is None:
        logging.error(f"Chat {chat.id} not found in database")
        return
    known_members = db_chat.members

    tasks = [chat.get_member(mem.user_id) for mem in known_members]
    members = await asyncio.gather(*tasks)
    tags = [utils.get_mention(mem.user) for mem in members]

    if tags:
        await message.answer(", ".join(tags), parse_mode="Markdown")
    else:
        logging.error(f"No users found in chat {chat.id}")


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(tag_all,
                                types.ChatType.is_group_or_super_group,
                                Command(["all"]) | Regexp(r"\B@all\b"),
                                is_user=True)
