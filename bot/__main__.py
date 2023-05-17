# from os import getenv
from typing import Any, Dict, Union
import sys

sys.path.append('D:/telegram_bot/contract_bot')
from aiohttp import web
from handlers import routers

from aiogram import Bot, Dispatcher,  Router
from aiogram.client.session.aiohttp import AiohttpSession
# from aiogram.exceptions import TelegramUnauthorizedError
# from aiogram.filters import Command, CommandObject
# from aiogram.fsm.storage.redis import DefaultKeyBuilder, RedisStorage
# from aiogram.types import Message
from aiogram.utils.token import TokenValidationError, validate_token
from aiogram.webhook.aiohttp_server import (
    SimpleRequestHandler,
    # TokenBasedRequestHandler,
    setup_application,
)
from bot.config import api_key
from bot.admin_panel import app
main_router = Router()

BASE_URL = "https://1926-109-252-118-219.ngrok-free.app"
MAIN_BOT_TOKEN = api_key

WEB_SERVER_HOST = "127.0.0.1"
WEB_SERVER_PORT = 8080
MAIN_BOT_PATH = "/webhook/main"
# OTHER_BOTS_PATH = "/webhook/bot/{bot_token}"


# REDIS_DSN = "redis://127.0.0.1:6479"

# OTHER_BOTS_URL = f"{BASE_URL}{OTHER_BOTS_PATH}"


def is_bot_token(value: str) -> Union[bool, Dict[str, Any]]:
    try:
        validate_token(value)
    except TokenValidationError:
        return False
    return True


async def on_startup(dispatcher: Dispatcher, bot: Bot):
    await bot.set_webhook(f"{BASE_URL}{MAIN_BOT_PATH}")


def main():
    session = AiohttpSession()
    bot_settings = {"session": session, "parse_mode": "HTML"}
    bot = Bot(token=MAIN_BOT_TOKEN, **bot_settings)
    # storage = RedisStorage.from_url(REDIS_DSN, key_builder=DefaultKeyBuilder(with_bot_id=True))

    main_dispatcher = Dispatcher()
    for router in routers:
        main_dispatcher.include_router(router)
    main_dispatcher.startup.register(on_startup)

    # multibot_dispatcher = Dispatcher(storage=storage)
    # for router in routers:
    #     multibot_dispatcher.include_router(router)

    # app = web.Application()
    SimpleRequestHandler(dispatcher=main_dispatcher, bot=bot).register(app, path=MAIN_BOT_PATH)
    # TokenBasedRequestHandler(
    #     dispatcher=multibot_dispatcher,
    #     bot_settings=bot_settings,
    # ).register(app, path=OTHER_BOTS_PATH)

    setup_application(app, main_dispatcher, bot=bot)
    # setup_application(app, multibot_dispatcher)

    web.run_app(app, host=WEB_SERVER_HOST, port=WEB_SERVER_PORT)


if __name__ == "__main__":
    main()
