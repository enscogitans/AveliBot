import asyncio
import datetime
import typing as tp

from aiogram import types
from dateparser import search


def search_dates(text: str, timezone: str, relative_base: datetime.datetime) -> tp.List[datetime.datetime]:
    settings = {
        "PREFER_DATES_FROM": "future",
        "RELATIVE_BASE": relative_base,
        "TIMEZONE": timezone,
        "RETURN_AS_TIMEZONE_AWARE": True
    }
    dates_info = search.search_dates(text, settings=settings) or []
    return [info[1] for info in dates_info]


async def sleep_until(deadline: datetime.datetime) -> None:
    while True:
        time_left = deadline - datetime.datetime.now(tz=datetime.timezone.utc)
        seconds_left = time_left.total_seconds()
        if seconds_left <= 0:
            break
        if seconds_left < 5:
            await asyncio.sleep(seconds_left)
        else:
            await asyncio.sleep(seconds_left / 2)


def get_mention(user: types.User) -> str:
    if user.username:
        return f"@{user.username}"
    return user.get_mention(as_html=True)
