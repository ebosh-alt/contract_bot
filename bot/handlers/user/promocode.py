from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.db import users, Flags

router = Router()


@router.message(lambda message: users.get(message.from_user.id).flag is Flags.input_promocode)
async def message_main(message: Message):
    id = message.from_user.id
    user = users.get(id)
    if message.text == "test":
        await SendMessage(chat_id=id,
                          text="На Ваш бонусный счет зачислено 10$",
                          reply_markup=kb.back_keyboard
                          )
        user.bonus_account += 10
        user.flag = Flags.NONE
    user.flag = Flags.NONE
    users.update_info(user)


promocode_router = router
