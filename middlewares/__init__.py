from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware
from sqlalchemy import orm

from .acl import ACLMiddleware


def register(dispatcher: Dispatcher, session: orm.Session) -> None:
    dispatcher.middleware.setup(LoggingMiddleware("bot"))
    dispatcher.middleware.setup(ACLMiddleware(session))
