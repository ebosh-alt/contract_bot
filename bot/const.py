from enum import Enum

Assets = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "USDT": "USDT",
}

procents = {
    30: {
        10: 0.03,
        100: 0.05,
        1000: 0.07,
        3000: 0.08,
        5000: 0.09,
        10000: 0.1
    },
    60: {
        10: 0.04,
        100: 0.06,
        1000: 0.08,
        3000: 0.09,
        5000: 0.1,
        10000: 0.12
    },
    90: {
        10: 0.05,
        100: 0.07,
        1000: 0.09,
        3000: 0.1,
        5000: 0.11,
        10000: 0.13
    }
}


class DAYS(Enum):
    count_30 = 30
    count_60 = 60
    count_90 = 90


class DEPOSIT(Enum):
    dep_10 = 10
    dep_100 = 100
    dep_1000 = 1000
    dep_3000 = 3000
    dep_5000 = 5000
    dep_10000 = 10000


Referral_procent = {
    "1_lvl": 0.3,
    "2_lvl": 0.2,
    "3_lvl": 0.1
}

