from aiogram import Dispatcher

from . import commands
from . import join_and_leave


def register(dp: Dispatcher) -> None:
    commands.register(dp)
    join_and_leave.register(dp)
