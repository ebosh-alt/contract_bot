import datetime

from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.db import users, Flags, Promocodes, promocodes, UserPromocode, userPromocodes

router = Router()


@router.message(lambda message: users.get(message.from_user.id).flag is Flags.input_promocode)
async def message_main(message: Message):
    id = message.from_user.id
    user = users.get(id)
    promocode = promocodes.get_by_name(name=message.text)
    if promocode:
        now = datetime.datetime.now()
        promocode_time = datetime.datetime.strptime(promocode.expiration_date, "%d/%m/%Y", )
        if promocode_time <= now or promocode.count_using == 0:
            del promocodes[promocode.id]
            await SendMessage(chat_id=id,
                              text=f"Такого промокода нет!",
                              reply_markup=kb.back_keyboard
                              )
        else:
            if userPromocodes.get_by_name(message.text) is False:
                user.bonus_account += promocode.amount
                promocode.count_using -= 1
                user_promocode = UserPromocode(id=len(userPromocodes)+1,
                                               name=promocode.name,
                                               user_id=id)
                userPromocodes.add(user_promocode)
                await SendMessage(chat_id=id,
                                  text=f"На Ваш бонусный счет зачислено {promocode.amount}$",
                                  reply_markup=kb.back_keyboard
                                  )
            else:
                await SendMessage(chat_id=id,
                                  text=f"Вы уже использовали данный промокод",
                                  reply_markup=kb.back_keyboard
                                  )
        promocodes.update_info(promocode)
    else:
        await SendMessage(chat_id=id,
                          text=f"Такого промокода нет!",
                          reply_markup=kb.back_keyboard
                          )
    users.update_info(user)


promocode_router = router
