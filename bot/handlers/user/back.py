from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.methods import SendMessage, EditMessageText, DeleteMessage
from aiogram.types import Message, CallbackQuery
from bot.db import users, contracts, Flags
from bot.utils import get_tmp
from bot import keyboards as kb

router = Router()


@router.message(lambda message: message.text == "Назад")
async def back_main_menu(message: Message):
    id = message.from_user.id
    m = await SendMessage(chat_id=id,
                          text=get_tmp("templates/text_by_menu.md"),
                          reply_markup=kb.main_keyboard)
    user = users.get(id)
    user.flag = Flags.NONE
    user.bot_message_id = m.message_id
    users.update_info(user)


@router.callback_query(lambda call: call.data in ("back", "choice_payment_method", "back_main", "back_profile",
                                                  "back_to_choice_price"))
async def call_back(call: CallbackQuery, state: FSMContext):
    id = call.from_user.id
    user = users.get(id)
    if user.status is False:
        await SendMessage(chat_id=id,
                          text="Вы заблокированы")
    elif call.data == "back":
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=get_tmp("templates/text_by_referral.md", referral_link=user.referral_link),
                              reply_markup=kb.statistics_referral_keyboard)

    elif call.data == "choice_payment_method":
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=get_tmp("templates/text_by_payment.md"),
                              reply_markup=kb.payment_method_keyboard)
    elif call.data == "back_profile":

        amount_of_contracts = sum([int(el[0]) for el in contracts.all_user_contracts(id)])

        mess = get_tmp(path="templates/text_by_profile.md", id=id, balance=user.balance,
                       amount_of_contracts=amount_of_contracts, earnings_contract=user.earnings_from_contracts,
                       earnings_referral=user.earnings_from_partners, bonus_account=user.bonus_account)

        await DeleteMessage(chat_id=id,
                            message_id=user.bot_message_id)
        m = await SendMessage(chat_id=id,
                              text=mess,
                              reply_markup=kb.keyboard_by_invest,
                              parse_mode="Markdown")

        user.bot_message_id = m.message_id
        users.update_info(user)

    elif call.data == "back_to_choice_price":
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text="Выберите сумму",
                              reply_markup=kb.deposit_contract_keyboard)
    await state.clear()

back_router = router
