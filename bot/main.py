import sys

sys.path.append('D:/telegram_bot/contract_bot')

from contextlib import suppress

import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import routers

from bot.config import api_key
# from bot.admin_panel import app
from bot.Processing import App


async def main() -> None:
    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)
    bot = Bot(api_key, parse_mode="Markdown")
    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        # filename="logger.log",
                        filemode="w",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')
    process = App()
    with suppress(KeyboardInterrupt):
        App.start_process(asyncio.run(main()))
