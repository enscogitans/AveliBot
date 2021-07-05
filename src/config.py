from envparse import env  # type: ignore


def get_telegram_token() -> str:
    return env.str("TELEGRAM_TOKEN")


def get_proxy_uri() -> str:
    return env.str("PROXY_URI", default="")


def get_proxy_login() -> str:
    return env.str("PROXY_LOGIN", default="")


def get_proxy_password() -> str:
    return env.str("PROXY_PASSWORD", default="")


def get_postgres_uri() -> str:
    host = env.str("POSTGRES_HOST")
    port = env.int("POSTGRES_PORT")
    user = env.str("POSTGRES_USER")
    password = env.str("POSTGRES_PASSWORD")
    db = env.str("POSTGRES_DB")
    return f"postgresql://{user}:{password}@{host}:{port}/{db}"
