from aiogram import Dispatcher

from .is_user import IsUser
from .is_reply import IsReply


def register(dispatcher: Dispatcher) -> None:
    dispatcher.filters_factory.bind(IsUser)
    dispatcher.filters_factory.bind(IsReply)
