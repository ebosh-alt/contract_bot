from aiogram import types
from aiogram.utils.keyboard import InlineKeyboardBuilder, ReplyKeyboardBuilder


def create_keyboard(name_buttons: list | dict, *sizes: int) -> types.InlineKeyboardMarkup:
    keyboard = InlineKeyboardBuilder()

    for name_button in name_buttons:
        if type(name_buttons[name_button]) is tuple:
            if len(name_buttons[name_button]) == 2:
                keyboard.button(
                    text=name_button, url=name_buttons[name_button][0], callback_data=name_buttons[name_button][1]
                )
            else:
                if "http" in name_buttons[name_button]:
                    keyboard.button(
                        text=name_button, url=name_button
                    )
                keyboard.button(
                    text=name_button, callback_data=name_button
                )

        else:

            if "http" in str(name_buttons[name_button]):
                keyboard.button(
                    text=name_button, url=name_buttons[name_button]
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
        if name_button is not tuple:
            keyboard.button(
                text=name_button
            )
        else:
            keyboard.button(
                text=name_button,

            )
    if len(sizes) == 0:
        sizes = (1,)
    keyboard.adjust(*sizes)
    return keyboard.as_markup(resize_keyboard=True, one_time_keyboard=one_time_keyboard)


name_button_main_keyboard = ["Инвестиционный счет", "Поддержка", "Партнерская программа", "Ответы на вопросы",
                             "Промокоды"]

main_keyboard = create_reply_keyboard(name_button_main_keyboard, False, 1, 2, 2)
back_keyboard = create_reply_keyboard(["Назад"])

keyboard_by_invest = create_reply_keyboard(["Новый контракт", "Мои контракты",
                                            "🔑Пополнить баланс", "↩️Вывести средства", "Назад"],
                                           True, 2, 2, 1)

statistics_referral_name_button = {
    "Показать 1-ый уровень": "watch_1_lvl",
    "Показать 2-ый уровень": "watch_2_lvl",
    "Показать 3-ый уровень": "watch_3_lvl"
}
statistics_referral_keyboard = create_keyboard(statistics_referral_name_button)

back_to_ref_keyboard = create_keyboard({"Назад": "back"})

payment_method_name_button = {
    "Bitcoin": "Bitcoin",
    "USDT-TRC20": "USDT",
    "Ethereum ERC-20": "Ethereum",
    "YMoney": "YMoney",
    "В ручном режиме": "В ручном режиме",
    "Назад": "back_profile"
}
payment_method_keyboard = create_keyboard(payment_method_name_button)

back_to_main_keyboard = create_keyboard({"Назад": "back_main"})

delete_notification_keyboard = create_keyboard({"Скрыть": "delete_notification"})

back_to_choice_payment = create_keyboard({"Назад": "choice_payment_method"})

back_to_profile_keyboard = create_keyboard({"Назад": "back_profile"})

replenishment_in_manual_mode_keyboard = create_keyboard(
    {"Готово": "ready_transaction", "Назад": "choice_payment_method"})

ymoney_keyboard = create_keyboard(
    {"Готово": "ready_ymoney", "Назад": "choice_payment_method"})

name_button_count_day = {
                        "30 дней": "30",
                        "60 дней": "60",
                        "90 дней": "90",
                        "Назад": "back_profile"
                         }
count_day_keyboard = create_keyboard(name_button_count_day)

name_button_deposit_contract = {
    "10$": "10",
    "100$": "100",
    "1000$": "1000",
    "3000$": "3000",
    "5000$": "5000",
    "10000$": "10000",
    "Назад": "back_to_choice_count_day"
}
deposit_contract_keyboard = create_keyboard(name_button_deposit_contract, 2, 2, 2, 1)

confirm_deposit_keyboard = create_keyboard({'✅ Заключить контракт': "confirm_contract", "Отменить": "back_profile"})


if __name__ == "__main__":
    print(payment_method_name_button.values())
