from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, AnswerCallbackQuery, EditMessageText, DeleteMessage
from aiogram.types import Message, CallbackQuery


from bot import keyboards as kb
from bot.States import States
from bot.db import users, Flags
from bot.utils import get_tmp
from bot.utils.CryptoPay import CryptoPay
from bot.utils.getPriceCoin import get_price_coin
from bot.utils.is_number_float import is_number_float
from bot.config import crypto_pay_key
from bot.const import Assets

router = Router()


@router.message(States.crypto)
async def ss(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    crypto_pay = CryptoPay(crypto_pay_key)
    amount = is_number_float(message.text)
    await DeleteMessage(chat_id=id,
                        message_id=message.message_id)
    if amount:
        data = await state.get_data()
        asset = data["crypto"]
        inv = await crypto_pay.create_invoice(asset=Assets[asset], amount=amount)
        await crypto_pay.close_session()
        await state.update_data(invoice_ids=inv.invoice_id)
        await state.update_data(amount=amount)
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=get_tmp("templates/text_by_pay_crypto_2.md"),
                              reply_markup=kb.create_keyboard(
                                  {"Оплатить": inv.pay_url, "Готово": "ready_paid_crypto",
                                   "Назад": "choice_payment_method"}),
                              parse_mode="Markdown")


@router.callback_query(States.crypto, lambda call: call.data == "ready_paid_crypto")
async def calls(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    data = await state.get_data()
    invoice_ids = data["invoice_ids"]
    crypto = data["crypto"]
    crypto_pay = CryptoPay(crypto_pay_key)
    try:
        inv = await crypto_pay.get_invoice(invoice_ids=invoice_ids)
        if inv.status == "paid" or True:
            amount = data['amount']

            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text='Пополнение прошло успешно')
            m = await SendMessage(chat_id=id,
                                  text=get_tmp("./templates/text_by_menu.md", username=user.username),
                                  reply_markup=kb.main_keyboard)
            price = get_price_coin(name=crypto) * amount
            if crypto == "USDT":
                price = float(amount)
            user.balance += price
            user.bot_message_id = m.message_id
            user.flag = Flags.NONE
            await state.clear()
            users.update_info(user)
        elif crypto == "expired":
            await AnswerCallbackQuery(callback_query_id=call.id,
                                      text="Ваш платеж просрочен! Попробуйте ещё раз",
                                      show_alert=True)
        else:
            await AnswerCallbackQuery(callback_query_id=call.id,
                                      text=get_tmp("templates/error_paid.md"),
                                      show_alert=True)
    except Exception:
        await AnswerCallbackQuery(callback_query_id=call.id,
                                  text=get_tmp("templates/error_paid.md"),
                                  show_alert=True)
    finally:
        await crypto_pay.close_session()

crypto_router = router
