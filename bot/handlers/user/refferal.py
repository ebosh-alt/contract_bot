from aiogram import Router
from aiogram.methods import EditMessageText, AnswerCallbackQuery
from aiogram.types import CallbackQuery
from bot.db import users
from bot.utils import get_tmp
from bot import keyboards as kb

router = Router()


@router.callback_query(lambda call: call.data in kb.statistics_referral_name_button.values())
async def call_statistic(call: CallbackQuery):
    id = call.from_user.id
    user = users.get(id)

    if call.data == "watch_1_lvl":
        lvl = 1
        bosses = users.get_ref_1_lvl(id)[0]
    elif call.data == "watch_2_lvl":
        lvl = 2
        bosses = users.get_ref_2_lvl(id)[0]
    else:
        lvl = 3
        bosses = users.get_ref_3_lvl(id)[0]
    temp = "\n".join(bosses)

    if len(bosses) == 0:
        await AnswerCallbackQuery(callback_query_id=call.id,
                                  text=get_tmp("templates/no_referral.md", lvl=lvl) ,
                                  show_alert=True)
    else:
        await EditMessageText(chat_id=id,
                              message_id=user.bot_message_id,
                              text=temp,
                              reply_markup=kb.back_to_ref_keyboard)


referral_router = router
