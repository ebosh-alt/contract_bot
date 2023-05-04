from aiogram import Router
from aiogram.methods import SendMessage, DeleteMessage, AnswerCallbackQuery
from aiogram.types import CallbackQuery

from bot.config import manager
from bot.db import users, Flags
from bot.utils import get_tmp
from bot import keyboards as kb
router = Router()


def check_manager(call: CallbackQuery):
    if call.from_user.id == manager:
        return True
    return False


@router.callback_query(lambda call: check_manager(call))
async def work_man(call: CallbackQuery):
    data = call.data.split("_")
    if len(data) >= 2:
        id = int(data[1])
        user = users.get(id)
        if data[0] == "yes":
            user.balance += float(data[2])
            await AnswerCallbackQuery(callback_query_id=call.id,
                                      text="Баланс пользователя пополнен",
                                      show_alert=True)
            await DeleteMessage(chat_id=manager,
                                message_id=call.message.message_id)
            await SendMessage(chat_id=id,
                              text=get_tmp("templates/replenishment_is_successful.md",
                                           count=float(data[2]), balance=user.balance),
                              reply_markup=kb.delete_notification_keyboard)
            users.update_info(user)

        elif data[0] == "no":
            await AnswerCallbackQuery(callback_query_id=call.id,
                                      text="Заявка отклонена",
                                      show_alert=True)
            await DeleteMessage(chat_id=manager,
                                message_id=call.message.message_id)
            await SendMessage(chat_id=id,
                              text=get_tmp("templates/replenishment_is_unsuccessful.md"),
                              reply_markup=kb.delete_notification_keyboard)
        user.flag = Flags.NONE
        users.update_info(user)


consideration_application_replenishment_router = router
