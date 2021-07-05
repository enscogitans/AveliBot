import asyncio
import typing as tp
from datetime import datetime

from aiogram import Bot
from sqlalchemy import orm

from models import ScheduledMessage
from utils.utils import sleep_until


def _del_from_db(session: orm.Session, chat_id: int, message_id: int) -> None:
    sched_msg = session.query(ScheduledMessage).get({"chat_id": chat_id, "message_id": message_id})
    session.delete(sched_msg)
    session.commit()


class MessageTask:
    def __init__(self, session: orm.Session, text: str, deadline: datetime, chat_id: int, message_id: int) -> None:
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
        await sleep_until(self.deadline)
        await bot.send_message(chat_id=self.chat_id, text=self.text, parse_mode="HTML")
        _del_from_db(self.session, self.chat_id, self.message_id)


class MessageScheduler:
    def __init__(self, session: orm.Session, bot: Bot):
        self.session = session
        self.bot = bot
        self.tasks: tp.Dict[tp.Tuple[int, int], asyncio.Task[None]] = dict()

    def _add_to_loop(self, message_task: MessageTask) -> None:
        loop = asyncio.get_event_loop()
        task_id = (message_task.chat_id, message_task.message_id)
        task = message_task.run(self.bot)
        self.tasks[task_id] = loop.create_task(task)

    def read_db(self) -> None:
        for sched_msg in self.session.query(ScheduledMessage).all():
            message_task = MessageTask(
                session=self.session,
                text=sched_msg.text, deadline=sched_msg.deadline,
                chat_id=sched_msg.chat_id, message_id=sched_msg.message_id
            )
            self._add_to_loop(message_task)

    def add_task(self, text: str, deadline: datetime,
                 chat_id: int, message_id: int) -> None:
        message_task = MessageTask(session=self.session,
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
