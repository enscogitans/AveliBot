from aiogram import Dispatcher

from . import commands, join_and_leave, schedule


def register(dp: Dispatcher) -> None:
    commands.register(dp)
    join_and_leave.register(dp)
    schedule.register(dp)
