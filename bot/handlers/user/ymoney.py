from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageText, SendMessage, DeleteMessage, AnswerCallbackQuery
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.States import States
from bot.db import users, Flags
from bot.utils import get_tmp
from bot.utils.YMoney.checkPay import check_pay
from bot.utils.YMoney.createPayment import create_pay
from bot.utils.get_rate import get_rate
from bot.utils.is_number_float import is_number_float

router = Router()


@router.message(States.ymoney)
async def inp_amount(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    amount = is_number_float(message.text)

    await DeleteMessage(chat_id=id,
                        message_id=message.message_id)
    if amount:
        if amount >= 10.0:

            data = create_pay(user_id=str(id), price=amount * float(get_rate()))
            link = data[0]
            key = data[1]

            await state.update_data(key=key)
            await state.update_data(amount=amount)

            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text=get_tmp("templates/text_by_ymoney.md"),
                                  reply_markup=kb.create_keyboard({"Оплатить": link, "Готово": "ymoney", "Назад": "choice_payment_method"}),
                                  parse_mode="Markdown")


        else:
            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text=get_tmp("templates/less_then_10.md", amount=amount),
                                  reply_markup=kb.back_to_choice_payment,
                                  parse_mode="Markdown")
    else:
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=get_tmp("templates/error_input_text.md", amount=amount),
                              reply_markup=kb.back_to_choice_payment,
                              parse_mode="Markdown")


@router.callback_query(lambda call: call.data == "ymoney")
async def call_statistic(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    data = await state.get_data()
    key = data['key']
    if check_pay(key):
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text='Пополнение прошло успешно')
        m = await SendMessage(chat_id=id,
                              text=get_tmp("./templates/text_by_menu.md", username=user.username),
                              reply_markup=kb.main_keyboard)
        await state.clear()
        user.balance += int(data["amount"])
        user.bot_message_id = m.message_id
        user.flag = Flags.NONE
        users.update_info(user)
    else:
        await AnswerCallbackQuery(callback_query_id=call.id,
                                  text="templates/error_paid.md",
                                  show_alert=True)
    users.update_info(user)


@router.callback_query(lambda call: call.data == "ready_ymoney")
@router.message(lambda message: message.photo)
async def inp_photo(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    data = await state.get_data()
    await state.clear()
    payment = check_pay(data['key'])
    print(payment)
    # user.bot_message_id = m.message_id
    # user.flag = Flags.awaiting_payment_confirmation
    users.update_info(user)


ymoney_router = router
