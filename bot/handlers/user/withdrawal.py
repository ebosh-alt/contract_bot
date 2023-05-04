from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, EditMessageText, DeleteMessage
from aiogram.types import Message

from bot import keyboards as kb
from bot.States import States
from bot.config import manager
from bot.db import users, Flags
from bot.utils import get_tmp
from bot.utils.is_number_float import is_number_float

router = Router()


@router.message(lambda message: message.text == "↩️Вывести средства")
async def withdrawal(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    m = await SendMessage(chat_id=id,
                          text=get_tmp("templates/withdrawal.md", balance=user.balance),
                          reply_markup=kb.back_to_profile_keyboard)
    user.bot_message_id = m.message_id
    await state.set_state(States.withdrawal.state)
    users.update_info(user)


@router.message(States.withdrawal)
async def input_withdrawal(message: Message, state: FSMContext):
    id = message.from_user.id
    user = users.get(id)
    amount = is_number_float(message.text)

    await DeleteMessage(chat_id=id,
                        message_id=message.message_id)
    if amount:
        if amount >= 10.0:
            if amount < user.balance:
                await SendMessage(chat_id=manager,
                                  text=get_tmp("templates/withdrawal_manager.md", fullname=user.username, id=user.id,
                                               balance=user.balance, amount=amount),
                                  reply_markup=kb.create_keyboard(name_buttons={"Подтвердить": f"yeswith_{id}_{amount}",
                                                                                "Отклонить": f"nowith_{id}"})
                                  )

                await EditMessageText(chat_id=id,
                                      message_id=user.bot_message_id,
                                      text='Ожидайте. Данные отправлены на модерацию')
                m = await SendMessage(chat_id=id,
                                      text=get_tmp("./templates/text_by_menu.md", username=user.username),
                                      reply_markup=kb.main_keyboard)
                user.bot_message_id = m.message_id
                user.flag = Flags.awaiting_withdrawal_confirmation
                users.update_info(user)
            else:
                await EditMessageText(chat_id=id,
                                      message_id=user.bot_message_id,
                                      text=get_tmp("templates/error_amount_withdrawal_more_balance.md"),
                                      reply_markup=kb.back_to_profile_keyboard,
                                      parse_mode="Markdown")
        else:
            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text=get_tmp("templates/less_then_10.md"),
                                  reply_markup=kb.back_to_profile_keyboard,
                                  parse_mode="Markdown")
    else:
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=get_tmp("templates/error_input_text.md"),
                              reply_markup=kb.back_to_profile_keyboard,
                              parse_mode="Markdown")


withdrawal_router = router
