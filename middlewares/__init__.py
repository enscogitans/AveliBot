from aiogram import Dispatcher
from aiogram.contrib.middlewares.logging import LoggingMiddleware

from .acl import ACLMiddleware


def register(dispatcher: Dispatcher) -> None:
    dispatcher.middleware.setup(LoggingMiddleware("bot"))
    dispatcher.middleware.setup(ACLMiddleware())
