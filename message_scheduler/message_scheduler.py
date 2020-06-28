import asyncio
import typing as tp
from datetime import datetime

from aiogram import Bot

from models import db, ScheduledMessage
from utils.utils import sleep_until


class MessageTask:
    def __init__(self, text: str, deadline: datetime, chat_id: int, message_id: int) -> None:
        self.text = text
        self.deadline = deadline
        self.chat_id = chat_id
        self.message_id = message_id

    def save_to_db(self) -> None:
        sched_msg = ScheduledMessage(text=self.text, deadline=self.deadline,
                                     chat_id=self.chat_id, message_id=self.message_id)
        db.add(sched_msg)
        db.commit()

    def del_from_db(self) -> None:
        sched_msg = db.query(ScheduledMessage) \
            .get({"chat_id": self.chat_id, "message_id": self.message_id})
        db.delete(sched_msg)
        db.commit()

    async def run(self, bot: Bot) -> None:
        await sleep_until(self.deadline)
        await bot.send_message(chat_id=self.chat_id, text=self.text,
                               reply_to_message_id=self.message_id)
        self.del_from_db()


class MessageScheduler:
    def __init__(self, bot: Bot):
        self.bot = bot
        self.tasks: tp.Dict[tp.Tuple[int, int], asyncio.Task[None]] = dict()

    def _add_to_loop(self, message_task: MessageTask) -> None:
        loop = asyncio.get_event_loop()
        task_id = (message_task.chat_id, message_task.message_id)
        task = message_task.run(self.bot)
        self.tasks[task_id] = loop.create_task(task)

    def read_db(self) -> None:
        for sched_msg in db.query(ScheduledMessage).all():
            message_task = MessageTask(
                text=sched_msg.text, deadline=sched_msg.deadline,
                chat_id=sched_msg.chat_id, message_id=sched_msg.message_id
            )
            self._add_to_loop(message_task)

    def add_task(self, text: str, chat_id: int, message_id: int, deadline: datetime) -> None:
        message_task = MessageTask(text=text, chat_id=chat_id,
                                   message_id=message_id, deadline=deadline)
        message_task.save_to_db()
        self._add_to_loop(message_task)

    def del_task(self, chat_id: int, message_id: int) -> None:
        task_id = (chat_id, message_id)
        task = self.tasks[task_id]
        task.cancel()

        sched_msg = db.query(ScheduledMessage).get({"chat_id": chat_id,
                                                    "message_id": message_id})
        db.delete(sched_msg)
        db.commit()
