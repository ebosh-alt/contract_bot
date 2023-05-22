from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.const import procents
from bot.db import users, contracts
from bot.utils import get_tmp

router = Router()


@router.message(lambda message: message.text == "Мои контракты")
async def ss(message: Message):
    id = message.from_user.id
    user = users.get(id)
    all_contract = contracts.all_user_contracts(id=id)
    mess = ""

    for contract in all_contract:
        if contract[5] == 1:
            procent = procents[contract[1]][contract[2]]

            mess += get_tmp("templates/contract.md", id=contract[0], count_day=contract[1], deposit=contract[2],
                            expiration_date=contract[6], procent=procent)
    m = await SendMessage(chat_id=id,
                          messsage_id=user.bot_message_id,
                          text=mess,
                          reply_markup=kb.back_to_profile_keyboard)
    user.bot_message_id = m.message_id
    users.update_info(user)


watch_contract_router = router
