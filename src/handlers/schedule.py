import asyncio
import datetime
import functools
import logging
import typing as tp

from aiogram import Bot, Dispatcher, types
from sqlalchemy import orm

from src.models import Chat, ScheduledMessage
from src import utils


def _del_from_db(session: orm.Session, chat_id: int, message_id: int) -> None:
    sched_msg = session.query(ScheduledMessage).get({"chat_id": chat_id, "message_id": message_id})
    session.delete(sched_msg)
    session.commit()


class _MessageTask:
    def __init__(self, session: orm.Session,
                 text: str, deadline: datetime.datetime,
                 chat_id: int, message_id: int) -> None:
        self.session = session
        self.text = text
        self.deadline = deadline
        self.chat_id = chat_id
        self.message_id = message_id

    def save_to_db(self) -> None:
        sched_msg = ScheduledMessage(text=self.text, deadline=self.deadline,
                                     chat_id=self.chat_id, message_id=self.message_id)
        self.session.add(sched_msg)
        self.session.commit()

    async def run(self, bot: Bot) -> None:
        await utils.sleep_until(self.deadline)
        await bot.send_message(chat_id=self.chat_id, text=self.text, parse_mode="HTML")
        _del_from_db(self.session, self.chat_id, self.message_id)


class _MessageScheduler:
    def __init__(self, session: orm.Session, bot: Bot):
        self.session = session
        self.bot = bot
        self.tasks: tp.Dict[tp.Tuple[int, int], asyncio.Task[None]] = dict()

    def _add_to_loop(self, message_task: _MessageTask) -> None:
        loop = asyncio.get_event_loop()
        task_id = (message_task.chat_id, message_task.message_id)
        task = message_task.run(self.bot)
        self.tasks[task_id] = loop.create_task(task)

    def read_db(self) -> None:
        for sched_msg in self.session.query(ScheduledMessage).all():
            message_task = _MessageTask(
                session=self.session,
                text=sched_msg.text, deadline=sched_msg.deadline,
                chat_id=sched_msg.chat_id, message_id=sched_msg.message_id
            )
            self._add_to_loop(message_task)

    def add_task(self, text: str, deadline: datetime.datetime,
                 chat_id: int, message_id: int) -> None:
        message_task = _MessageTask(session=self.session,
                                    text=text, chat_id=chat_id,
                                    message_id=message_id, deadline=deadline)
        message_task.save_to_db()
        self._add_to_loop(message_task)

    def del_task(self, chat_id: int, message_id: int) -> bool:
        task_id = (chat_id, message_id)
        if task_id not in self.tasks:
            return False
        self.tasks[task_id].cancel()
        del self.tasks[task_id]
        _del_from_db(self.session, chat_id, message_id)
        return True


async def schedule(session: orm.Session, scheduler: _MessageScheduler, message: types.Message) -> None:
    db_chat = session.query(Chat).get(message.chat.id)
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

    command = message.get_command()
    text = message.html_text.lstrip(command)
    scheduler.add_task(text, deadline, message.chat.id, bot_message.message_id)


async def unschedule(scheduler: _MessageScheduler, message: types.Message) -> None:
    if scheduler.del_task(message.chat.id, message.reply_to_message.message_id):
        await message.reply("Запланированное сообщение отменено")
    else:
        await message.reply("Ничего не запланировано, отменять нечего")


def register(dp: Dispatcher, session: orm.Session) -> None:
    scheduler = _MessageScheduler(session, dp.bot)
    dp.register_message_handler(functools.partial(schedule, session, scheduler),
                                is_user=True,
                                is_group_or_supergroup=True,
                                commands=["schedule", "sched"])
    dp.register_message_handler(functools.partial(unschedule, scheduler),
                                is_user=True,
                                is_group_or_supergroup=True,
                                is_reply=True,
                                commands=["unschedule", "unsched"])
