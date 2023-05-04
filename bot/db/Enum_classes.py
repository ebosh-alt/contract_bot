from enum import Enum


class Flags(Enum):
    NONE = 0
    input_promocode = 1
    awaiting_payment_confirmation = 2
    awaiting_withdrawal_confirmation = 3



class Admin_flags(Enum):
    NONE = 0
    input_user_b = 1


class Reminder(Enum):
    NONE = 0
    first_reminder = 1
    second_reminder = 2
    third_reminder = 3
    fourth_reminder = 4
