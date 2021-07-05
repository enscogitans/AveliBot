import logging
import typing as tp

from aiogram import Bot, Dispatcher
from aiogram.utils.executor import Executor
from aiohttp import BasicAuth
from sqlalchemy import create_engine, orm

from src import config, filters, handlers, middlewares


def setup_proxy() -> tp.Tuple[tp.Optional[str], tp.Optional[BasicAuth]]:
    uri = config.get_proxy_uri()
    if not uri:
        return None, None
    if not config.get_proxy_login():
        return uri, None
    return uri, BasicAuth(login=config.get_proxy_login(), password=config.get_proxy_password())


def setup() -> tp.Tuple[Dispatcher, Executor]:
    logging.basicConfig(level=logging.INFO)

    engine = create_engine(config.get_postgres_uri())
    session = orm.Session(engine)

    proxy, proxy_auth = setup_proxy()
    bot = Bot(token=config.get_telegram_token(), proxy=proxy, proxy_auth=proxy_auth)

    dispatcher = Dispatcher(bot)
    filters.register(dispatcher)
    middlewares.register(dispatcher, session)
    handlers.register(dispatcher, session)

    executor = Executor(dispatcher, skip_updates=True)
    return dispatcher, executor


if __name__ == "__main__":
    dispatcher, executor = setup()
    executor.start_polling(dispatcher)
