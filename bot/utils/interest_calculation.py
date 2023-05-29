import asyncio

from aiogram import Bot
from schedule import every, repeat, run_pending
import time
from multiprocessing import Process

from bot.utils import get_tmp
from bot.config import api_key
from bot.db import users, User, contracts, Contract
from bot.const import procents
import datetime
from bot.config import bot


async def send(id: int, id_contract: int, amount: float):
    txt = f"На Ваш счет начислено **{amount}$** за контракт **#{id_contract}**!"
    await bot.send_message(chat_id=id,
                           text=txt)


@repeat(every().day)
def interest_calculation():
    for contract in contracts:
        if contract.status is True:
            procent = procents[contract.count_day][contract.amount]
            user = users.get(contract.user_id)
            if user.id != 686171972:
                continue
            amount = contract.amount * procent
            user.balance += amount
            now = datetime.datetime.now()
            contract_time = datetime.datetime.strptime(contract.expiration_date, "%d/%m/%Y", )
            if contract_time <= now:
                contract.status = False
            loop = asyncio.get_event_loop()
            loop.run_until_complete(send(id=user.id, id_contract=contract.id, amount=amount))
            users.update_info(user)
            contracts.update_info(contract)


class Interest_calculation:
    def __init__(self) -> None:
        self.p0 = Process()

    def start_process(self, func, arg=None):
        if arg is not None:
            self.p0 = Process(target=func, args=(arg,))
        else:
            self.p0 = Process(target=func)
        self.p0.start()

    def stop_process(self):
        self.p0.terminate()

    @staticmethod
    def work():
        run_pending()

    def start_schedule(self):
        while True:
            self.work()
            time.sleep(60*60*4)


if __name__ == "__main__":
    reminders = Interest_calculation()
    reminders.start_process(func=reminders.start_schedule)
