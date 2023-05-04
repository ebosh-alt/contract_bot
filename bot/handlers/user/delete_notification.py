from aiogram import Router
from aiogram.methods import DeleteMessage
from aiogram.types import CallbackQuery

router = Router()


@router.callback_query(lambda call: call.data == "delete_notification")
async def delete_notification(call: CallbackQuery):
    await DeleteMessage(chat_id=call.from_user.id,
                        message_id=call.message.message_id)


delete_notification_router = router
