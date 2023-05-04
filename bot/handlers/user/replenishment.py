from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, AnswerCallbackQuery, EditMessageText
from aiogram.types import Message, CallbackQuery

from bot import keyboards as kb
from bot.States import States
from bot.db import users, Flags
from bot.utils import get_tmp

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
    m = await SendMessage(chat_id=id,
                          text=get_tmp("templates/text_by_payment.md"),
                          reply_markup=kb.payment_method_keyboard)
    user.bot_message_id = m.message_id
    users.update_info(user)


# {'bot': <aiogram.client.bot.Bot object at 0x000001AE634FC610>, 'storage': <aiogram.fsm.storage.memory.MemoryStorage object at 0x000001AE634FC350>, 'key': StorageKey(bot_id=6233322844, chat_id=686171972, user_id=686171972, destiny='default')}

@router.callback_query(lambda call: call.data in kb.payment_method_name_button.values())
async def call_statistic(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)

    if call.data == "В ручном режиме":
        if user.flag is Flags.awaiting_payment_confirmation:
            await AnswerCallbackQuery(callback_query_id=call.id,
                                      text="Вы уже отправили на модерацию платеж. Подождите...",
                                      show_alert=True)
        else:
            await EditMessageText(chat_id=id,
                                  message_id=user.bot_message_id,
                                  text=get_tmp("templates/text_by_replenishment_in_manual_mode.md"),
                                  reply_markup=kb.back_to_choice_payment,
                                  parse_mode="Markdown")
            await state.set_state(States.deposit.state)
    users.update_info(user)


replenishment_router = router
