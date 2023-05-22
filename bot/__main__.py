import asyncio
import sys
from multiprocessing import Process

sys.path.append('D:/telegram_bot/contract_bot')
from bot.utils.delFolder import del_folder


import threading
from contextlib import suppress
import logging
from aiogram import Bot, Dispatcher

from bot.handlers import routers
from bot.config import api_key
from bot.admin_panel import app


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
    with suppress(KeyboardInterrupt):
        del_folder("D:/telegram_bot/contract_bot/bot/admin_panel/photo")

        asyncio.run(main())
        app.run()
        threading.Thread(target=lambda: asyncio.run(main())).start()
        p0 = Process(target=app.run())
        p0.start()
