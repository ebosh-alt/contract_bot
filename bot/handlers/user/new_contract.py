import datetime

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import EditMessageText, SendMessage, AnswerCallbackQuery
from aiogram.types import CallbackQuery, Message

from bot import keyboards as kb
from bot.States import States
from bot.const import procents
from bot.db import users, Flags, contracts, Contract
from bot.utils import get_tmp

router = Router()


@router.message(lambda message: message.text == "Новый контракт")
async def ss(message: Message):
    id = message.from_user.id
    user = users.get(id)
    m = await SendMessage(chat_id=id,
                          text="Выберите сумму",
                          reply_markup=kb.deposit_contract_keyboard)

    user.bot_message_id = m.message_id

    users.update_info(user)


@router.callback_query(lambda call: call.data in kb.name_button_deposit_contract.values() and "back" not in call.data)
async def ass(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    await state.set_state(States.contract)
    deposit = int(call.data)
    if deposit <= user.balance + user.bonus_account:
        await state.update_data(deposit=deposit)
        # data = await state.get_data()
        # count_day = data["count_day"]
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text="Выберите на какое количество дней",
                              reply_markup=kb.count_day_keyboard)


    else:
        await AnswerCallbackQuery(callback_query_id=call.id,
                                  text='На счету не достаточно средств',
                                  show_alert=True)

    await state.update_data(deposit=int(call.data))




@router.callback_query(States.contract,
                       lambda call: call.data in kb.name_button_count_day.values() and "back" not in call.data)
async def ass(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    data = await state.get_data()
    deposit = int(data["deposit"])
    count_day = int(call.data)
    procent = procents[count_day][deposit]
    await state.update_data(count_day=count_day)

    await EditMessageText(chat_id=id,
                          message_id=user.bot_message_id,
                          text=get_tmp("templates/text_by_confirm_contract.md", id=len(contracts) + 1,
                                       count_day=count_day, deposit=deposit, procent=procent),
                          reply_markup=kb.confirm_deposit_keyboard,
                          parse_mode="Markdown")


@router.callback_query(States.contract, lambda call: call.data == "confirm_contract")
async def ass(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    data = await state.get_data()
    count_day = data["count_day"]
    amount = data["deposit"]
    expiration_date = (datetime.datetime.now() + datetime.timedelta(days=count_day)).strftime("%d/%m/%Y")
    procent = procents[count_day][amount]
    contract = Contract(id=len(contracts)+1,
                        count_day=count_day,
                        amount=amount,
                        user_id=id,
                        procent=procent,
                        status=True,
                        expiration_date=expiration_date)
    contracts.add(contract)
    bonus_account = user.bonus_account

    if bonus_account <= amount:
        amount -= bonus_account
        user.balance -= amount
        user.bonus_account = 0
    elif bonus_account >= amount:
        user.bonus_account -= amount

    await EditMessageText(chat_id=id,
                          message_id=user.bot_message_id,
                          text='Контракт успешно добавлен')
    m = await SendMessage(chat_id=id,
                          text=get_tmp("./templates/text_by_menu.md", username=user.username),
                          reply_markup=kb.main_keyboard,
                          parse_mode="Markdown")
    await state.clear()
    # user.balance -= int(data["deposit"])
    user.bot_message_id = m.message_id
    user.flag = Flags.NONE
    users.update_info(user)
new_contact_router = router
