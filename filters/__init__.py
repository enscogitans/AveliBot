from aiogram import Dispatcher

from .is_user import IsUser


def register(dispatcher: Dispatcher) -> None:
    dispatcher.filters_factory.bind(IsUser)
