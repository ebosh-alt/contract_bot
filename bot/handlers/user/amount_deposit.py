import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageText, SendMessage, SendPhoto, DeleteMessage
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.States import States
from bot.config import manager
from bot.db import users, Flags
from bot.utils import get_tmp
from bot.utils.is_number_float import is_number_float

router = Router()


@router.message(States.deposit, lambda message: message.photo is None)
async def inp_amount(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    amount = is_number_float(message.text)

    await DeleteMessage(chat_id=id,
                        message_id=message.message_id)
    if amount:
        if amount >= 10.0:
            await state.update_data(deposit=amount)
            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text=get_tmp("templates/text_by_replenishment_in_manual_mode_2.md", amount=amount),
                                  reply_markup=kb.replenishment_in_manual_mode_keyboard,
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


@router.callback_query(lambda call: call.data == "ready_transaction")
async def call_statistic(call: CallbackQuery):
    id = call.from_user.id
    user = users.get(id)
    await EditMessageText(chat_id=id,
                          message_id=user.bot_message_id,
                          reply_markup=kb.back_to_choice_payment,
                          text="Оправьте скриншот")
    users.update_info(user)


@router.message(lambda message: message.photo)
async def inp_photo(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    data = await state.get_data()
    await state.clear()
    logging.info(data)
    await DeleteMessage(chat_id=id,
                        message_id=message.message_id)
    await EditMessageText(chat_id=id,
                          message_id=user.bot_message_id,
                          text='Ожидайте. Данные отправлены на модерацию')
    m = await SendMessage(chat_id=id,
                          text=get_tmp("./templates/text_by_menu.md", username=user.username),
                          reply_markup=kb.main_keyboard)
    await SendPhoto(chat_id=manager,
                    photo=message.photo[0].file_id,
                    caption=get_tmp("templates/text_by_replenishment_manager.md", fullname=user.username, id=user.id,
                                    balance=user.balance, amount=data['deposit']),
                    reply_markup=kb.create_keyboard(name_buttons={"Подтвердить": f"yes_{id}_{data['deposit']}",
                                                                  "Отклонить": f"no_{id}"}))
    user.bot_message_id = m.message_id
    user.flag = Flags.awaiting_payment_confirmation
    users.update_info(user)


amount_deposit_router = router
