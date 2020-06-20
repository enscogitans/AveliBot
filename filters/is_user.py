from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters.filters import BoundFilter


@dataclass
class IsUser(BoundFilter):  # type: ignore
    key = "is_user"
    is_user: bool

    async def check(self, message: types.Message) -> bool:
        return self.is_user != message.from_user.is_bot
