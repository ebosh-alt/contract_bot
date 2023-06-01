import asyncio
import sys

sys.path.append('D:/telegram_bot/contract_bot')
from multiprocessing import Process

from bot.utils.interest_calculation import Interest_calculation
import threading
from contextlib import suppress
import logging

from bot.handlers import routers
from bot.config import bot, dp, host, port
from bot.admin_panel import app


async def main() -> None:
    for router in routers:
        dp.include_router(router)

    await dp.start_polling(bot)


if __name__ == "__main__":
    logging.basicConfig(level=logging.INFO,
                        # filename="logger.log",
                        filemode="w",
                        format="%(levelname)s %(asctime)s %(message)s",
                        encoding='utf-8')

    with suppress(KeyboardInterrupt):

        asyncio.run(main())
        # interest_calculation = Interest_calculation()
        # interest_calculation.start_process(func=interest_calculation.start_schedule)
        # threading.Thread(target=lambda: app.run(host=host, port=port)).start()
        # p0 = Process(target=asyncio.run(main()))
        # p0.start()

