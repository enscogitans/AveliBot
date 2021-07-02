import datetime
import logging

from aiogram import Dispatcher, types

from message_scheduler import get_scheduler
from models import Chat, db
from utils import utils


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

    bot_message = await message.reply(f"Запланировано на {deadline.strftime('%d.%m.%y %H:%M:%S')}")
    scheduler = get_scheduler()

    command = message.get_command()
    text = message.html_text.lstrip(command)
    scheduler.add_task(text, deadline, message.chat.id, bot_message.message_id)


async def unschedule(message: types.Message) -> None:
    scheduler = get_scheduler()
    if scheduler.del_task(message.chat.id, message.reply_to_message.message_id):
        await message.reply("Запланированное сообщение отменено")
    else:
        await message.reply("Ничего не запланировано, отменять нечего")


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(schedule,
                                is_user=True,
                                is_group_or_supergroup=True,
                                commands=["schedule", "sched"])
    dp.register_message_handler(unschedule,
                                is_user=True,
                                is_group_or_supergroup=True,
                                is_reply=True,
                                commands=["unschedule", "unsched"])
