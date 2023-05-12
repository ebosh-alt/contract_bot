from aiogram import Router
from aiogram.methods import SendMessage
from aiogram.types import Message
from bot.db import users, contracts, Flags
from bot.utils import get_tmp
from bot import keyboards as kb

router = Router()


@router.message(lambda message: message.text in kb.name_button_main_keyboard)
async def message_main(message: Message):
    id = message.from_user.id
    user = users.get(id)
    if message.text == "Инвестиционный счет":
        amount_of_contracts = sum([int(el[2]) for el in contracts.all_user_contracts(id)])

        mess = get_tmp(path="templates/text_by_profile.md", id=id, balance=user.balance,
                       amount_of_contracts=amount_of_contracts, earnings_contract=user.earnings_from_contracts,
                       earnings_referral=user.earnings_from_partners, bonus_account=user.bonus_account)
        m = await SendMessage(chat_id=id,
                              text=mess,
                              reply_markup=kb.keyboard_by_invest,
                              parse_mode="Markdown")

    elif message.text == "Поддержка":
        m = await SendMessage(chat_id=id,
                              text=get_tmp("templates/text_support.md"),
                              reply_markup=kb.back_keyboard)

    elif message.text == "Партнерская программа":
        text = get_tmp("templates/text_by_referral.md", referral_link=user.referral_link)
        m = await SendMessage(chat_id=id,
                              text=text,
                              reply_markup=kb.statistics_referral_keyboard)

    elif message.text == "Ответы на вопросы":
        m = await SendMessage(chat_id=id,
                              text=get_tmp("templates/text_by_faq.md"),
                              reply_markup=kb.back_keyboard)

    # elif message.text == "Промокоды":
    else:
        m = await SendMessage(chat_id=id,
                              text=get_tmp("templates/text_by_promocode.md"),
                              reply_markup=kb.back_keyboard)
        user.flag = Flags.input_promocode

    user.bot_message_id = m.message_id
    users.update_info(user)


main_router = router
