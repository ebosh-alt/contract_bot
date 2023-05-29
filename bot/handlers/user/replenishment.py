from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, AnswerCallbackQuery, EditMessageText
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.States import States
from bot.db import users, Flags
from bot.utils import get_tmp
from bot.utils.get_rate import get_rate
from bot.utils.getPriceCoin import get_price_coin
router = Router()


def is_number_float(el):
    """ Returns True if string is a number. """
    try:
        if el in ",":
            el = el.replace(",", ".")
        float(el)
        return float(el)
    except ValueError:
        return False


@router.message(lambda message: message.text == "🔑Пополнить баланс")
async def message_main(message: Message):
    id = message.from_user.id
    user = users.get(id)
    if user.status is False:
        await SendMessage(chat_id=id,
                          text="Вы заблокированы")
    else:
        m = await SendMessage(chat_id=id,
                              text=get_tmp("templates/text_by_payment.md"),
                              reply_markup=kb.payment_method_keyboard)
        user.bot_message_id = m.message_id
        users.update_info(user)


@router.callback_query(lambda call: call.data in kb.payment_method_name_button.values() and "back" not in call.data)
async def call_statistic(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    if user.flag is Flags.awaiting_payment_confirmation and call.data == "В ручном режиме":
        await AnswerCallbackQuery(callback_query_id=call.id,
                                  text="Вы уже отправили на модерацию платеж. Подождите...",
                                  show_alert=True)
    if call.data == "В ручном режиме":
        await state.set_state(States.deposit.state)

    elif call.data == "YMoney":
        await state.set_state(States.ymoney.state)

    else:
        await state.set_state(States.crypto.state)
        await state.update_data(crypto=call.data)
        price = get_price_coin(name=call.data)
        if call.data == "USDT":
            price = 1.0

        return await EditMessageText(chat_id=id,
                                     message_id=user.bot_message_id,
                                     text=get_tmp("templates/text_by_pay_crypto.md",
                                                  price=price,
                                                  crypto=call.data),
                                     reply_markup=kb.back_to_choice_payment,
                                     parse_mode="Markdown")

    await EditMessageText(chat_id=id,
                          message_id=user.bot_message_id,
                          text=get_tmp("templates/text_by_replenishment_in_manual_mode.md", rate=get_rate()),
                          reply_markup=kb.back_to_choice_payment,
                          parse_mode="Markdown")


replenishment_router = router
