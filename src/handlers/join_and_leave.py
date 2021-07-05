from aiogram import Dispatcher, types


async def on_users_join(message: types.Message) -> None: ...


async def on_user_leave(message: types.Message) -> None: ...


def register(dp: Dispatcher) -> None:
    dp.register_message_handler(on_users_join,
                                is_user=True,
                                is_group_or_supergroup=True,
                                content_types=types.ContentTypes.NEW_CHAT_MEMBERS)
    dp.register_message_handler(on_user_leave,
                                is_user=True,
                                is_group_or_supergroup=True,
                                content_types=types.ContentTypes.LEFT_CHAT_MEMBER)
