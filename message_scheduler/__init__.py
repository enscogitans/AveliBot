import typing as tp

from aiogram import Bot

from .message_scheduler import MessageScheduler

_scheduler: tp.Optional[MessageScheduler] = None


def register(bot: Bot) -> None:
    global _scheduler
    _scheduler = MessageScheduler(bot)
    _scheduler.read_db()


def get_scheduler() -> MessageScheduler:
    if _scheduler is None:
        raise RuntimeError("MessageScheduler was not initialized via `register`")
    return _scheduler
