import logging

from aiogram import Dispatcher
from aiogram.utils.executor import Executor

# import all the models so that Alembic could see them
from .chat import Chat
from .chat_member import ChatMember
from .db import db
from .user import User

__all__ = ["db", "setup", "Chat", "ChatMember", "User"]


def setup(executor: Executor, postgres_uri: str) -> None:
    async def on_startup(dispatcher: Dispatcher) -> None:
        logging.getLogger("gino.engine").setLevel(logging.WARNING)
        await db.set_bind(postgres_uri, echo=False)

    async def on_shutdown(dispatcher: Dispatcher) -> None:
        bind = db.pop_bind()
        if bind:
            await bind.close()

    executor.on_startup(on_startup)
    executor.on_shutdown(on_shutdown)
