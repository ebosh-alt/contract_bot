from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder, ReplyKeyboardMarkup


def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for name_button in name_buttons:
        if type(name_button) is list:
            keyboard.button(
                text=name_button, callback_data=name_button
            )

        else:
            keyboard.button(
                text=name_button, callback_data=name_buttons[name_button]
            )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=True)


def create_reply_keyboard(name_buttons: list, one_time_keyboard: bool = False, *sizes) -> types.ReplyKeyboardMarkup:
    keyboard = ReplyKeyboardBuilder()

    for name_button in name_buttons:
        keyboard.button(
            text=name_button
        )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


name_button_main_keyboard = ["Инвестиционный счет", "Поддержка", "Партнерская программа", "Ответы на вопросы",
                             "Промокоды"]

main_keyboard = create_reply_keyboard(name_button_main_keyboard, False, 1, 2, 2)
back_keyboard = create_reply_keyboard(["Назад"])

keyboard_by_invest = create_reply_keyboard(["🔑Пополнить баланс", "Назад"], one_time_keyboard=True)

statistics_referral_name_button = {
    "Показать 1-ый уровень": "watch_1_lvl",
    "Показать 2-ый уровень": "watch_2_lvl",
    "Показать 3-ый уровень": "watch_3_lvl"
}
statistics_referral_keyboard = create_keyboard(statistics_referral_name_button)

back_to_ref_keyboard = create_keyboard({"Назад": "back"})

payment_method_name_button = {
    "Bitcoin": "Bitcoin",
    "USDT-TRC20": "USDT-TRC20",
    "Ethereum ERC-20": "Ethereum ERC-20",
    "FreeKassa": "FreeKassa",
    "В ручном режиме": "В ручном режиме",
    "Назад": "back_main"
}
payment_method_keyboard = create_keyboard(payment_method_name_button)

back_to_main_keyboard = create_keyboard({"Назад": "back_main"})

delete_notification_keyboard = create_keyboard({"Скрыть": "delete_notification"})

back_to_choice_payment = create_keyboard({"Назад": "choice_payment_method"})

replenishment_in_manual_mode_keyboard = create_keyboard(
    {"Готово": "ready_transaction", "Назад": "choice_payment_method"})
