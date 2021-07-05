from aiogram import Dispatcher

from .is_group_or_supergroup import IsGroupOrSupergroup
from .is_reply import IsReply
from .is_user import IsUser


def register(dispatcher: Dispatcher) -> None:
    dispatcher.filters_factory.bind(IsReply)
    dispatcher.filters_factory.bind(IsUser)
    dispatcher.filters_factory.bind(IsGroupOrSupergroup)
