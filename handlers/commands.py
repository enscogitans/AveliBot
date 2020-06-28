import asyncio
import datetime
import logging

from aiogram import types, Dispatcher
from aiogram.dispatcher.filters import Command, Regexp

from message_scheduler import get_scheduler
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


async def schedule(message: types.Message) -> None:
    db_chat = db.query(Chat).get(message.chat.id)
    if db_chat is None:
        logging.error(f"Chat {message.chat.id} not found in database")
        return

    dates = utils.search_dates(message.get_args(), db_chat.timezone, message.date)
    if not dates:
        await message.reply("Не могу найти дату :(")
        return

    deadline = dates[0]
    if deadline < datetime.datetime.now(tz=datetime.timezone.utc):
        await message.reply("Эта дата уже прошла!")
        return

    await message.reply(f"Запланировано на {deadline.strftime('%d.%m.%y %H:%M:%S')}")
    scheduler = get_scheduler()
    scheduler.add_task(message.get_args(), message.chat.id, message.message_id, deadline)


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(tag_all,
                                types.ChatType.is_group_or_super_group,
                                Command(["all"]) | Regexp(r"\B@all\b"),
                                is_user=True)
    dp.register_message_handler(schedule,
                                types.ChatType.is_group_or_super_group,
                                is_user=True, commands=["schedule", "sched"])
