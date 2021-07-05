from dataclasses import dataclass

from aiogram import types
from aiogram.dispatcher.filters.filters import BoundFilter


@dataclass
class IsGroupOrSupergroup(BoundFilter):  # type: ignore
    key = "is_group_or_supergroup"
    is_group_or_supergroup: bool

    async def check(self, message: types.Message) -> bool:
        res: bool = message.chat.type in (types.ChatType.GROUP, types.ChatType.SUPERGROUP)
        return self.is_group_or_supergroup == res
