from aiogram import Dispatcher
from sqlalchemy import orm

from . import commands, join_and_leave, schedule, wolf_game


def register(dp: Dispatcher, session: orm.Session) -> None:
    commands.register(dp, session)
    join_and_leave.register(dp)
    schedule.register(dp, session)
    wolf_game.register(dp, session)
