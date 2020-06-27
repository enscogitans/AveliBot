import logging
import typing as tp

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from aiohttp import BasicAuth

import config
import filters
import handlers
import middlewares


def setup_proxy() -> tp.Tuple[tp.Optional[str], tp.Optional[BasicAuth]]:
    if not config.PROXY_URI:
        return None, None
    if not config.PROXY_LOGIN:
        return config.PROXY_URI, None
    return config.PROXY_URI, BasicAuth(login=config.PROXY_LOGIN, password=config.PROXY_PASSWORD)


def setup() -> tp.Tuple[Dispatcher, Executor]:
    logging.basicConfig(level=logging.INFO)

    proxy, proxy_auth = setup_proxy()
    bot = Bot(token=config.TELEGRAM_TOKEN, proxy=proxy, proxy_auth=proxy_auth)
    dp = Dispatcher(bot)

    filters.register(dp)
    middlewares.register(dp)
    handlers.register(dp)

    executor = Executor(dp, skip_updates=True)
    return dp, executor


def main() -> None:
    dp, executor = setup()
    executor.start_polling(dp)


if __name__ == "__main__":
    main()
