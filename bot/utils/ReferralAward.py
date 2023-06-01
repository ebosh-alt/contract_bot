from aiogram.methods import SendMessage

from bot.const import Referral_procent
from bot.db import User, users
from bot.utils import get_tmp


async def accrual(id_users: list, amount: float):
    for id in id_users:
        boss_user = users.get(id)
        boss_user.balance += amount
        await SendMessage(chat_id=id,
                          text=get_tmp("templates/referral_award.md", amount=amount, username=boss_user.username))


async def referralAward(id: int, amount: float):
    await accrual(users.get_ref_1_lvl(id)[1], amount * Referral_procent["1_lvl"])
    await accrual(users.get_ref_2_lvl(id)[1], amount * Referral_procent["2_lvl"])
    await accrual(users.get_ref_3_lvl(id)[1], amount * Referral_procent["3_lvl"])

### вставить в моменты пополнения счета пользователям
