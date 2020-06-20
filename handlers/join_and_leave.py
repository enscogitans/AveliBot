from aiogram import types, Dispatcher


async def on_users_join(message: types.Message) -> None: ...


async def on_user_leave(message: types.Message) -> None: ...


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(on_users_join,
                                types.ChatType.is_group_or_super_group,
                                is_user=True,
                                content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(on_user_leave,
                                types.ChatType.is_group_or_super_group,
                                is_user=True,
                                content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
