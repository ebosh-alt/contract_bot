import sys
sys.path.append('D:/telegram_bot/contract_bot')

from contextlib import suppress

import logging
import asyncio
from aiogram import Bot, Dispatcher
from handlers import routers


async def main() -> None:
    dp = Dispatcher()
    for router in routers:
        dp.include_router(router)
    api_key = "6233322844:AAGQeeaiwLKmsCE3ZsUjbegj6TsIrdpJSzE"
    bot = Bot(api_key, parse_mode="Markdown")

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        # filename="logger.log",
                        filemode="w",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')
    with suppress(KeyboardInterrupt):
        asyncio.run(main())
