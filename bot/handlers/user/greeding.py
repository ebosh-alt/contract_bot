from aiogram import types, Router
from aiogram.filters import CommandStart
from aiogram.methods import SendMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.config import link_to_bot
from bot.db import users, User
from bot.utils import get_tmp

router = Router()


def add_user(message: Message):
    id = message.from_user.id
    users.add(User(id))
    user = users.get(id)
    user.referral_link = f"{link_to_bot}?start={id}"
    mes = message.text.split(" ")
    user.username = " ".join(message.from_user.full_name.split(" "))

    if len(mes) == 2:
        user.referral_boss_id = int(mes[1])
    users.update_info(user)


@router.message(CommandStart())
async def main_menu(message: types.Message):
    id = message.from_user.id
    if id not in users:
        add_user(message)

    user = users.get(id)
    if user.status is False:
        await SendMessage(chat_id=id,
                          text="Вы заблокированы")
    else:
        m = await SendMessage(chat_id=id,
                              text=get_tmp("./templates/text_by_menu.md", username=user.username),
                              reply_markup=kb.main_keyboard)
        user.bot_message_id = m.message_id
        users.update_info(user)


start_router = router
