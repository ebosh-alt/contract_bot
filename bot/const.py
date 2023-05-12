from enum import Enum

Assets = {
    "Bitcoin": "BTC",
    "Ethereum": "ETH",
    "USDT": "USDT",
}

procents = {
    30: {
        10: 0.3,
        100: 0.5,
        1000: 0.7,
        3000: 0.8,
        5000: 0.9,
        10000: 1.1
    },
    60: {
        10: 0.4,
        100: 0.6,
        1000: 0.8,
        3000: 0.9,
        5000: 1,
        10000: 1.2
    },
    90: {
        10: 0.5,
        100: 0.7,
        1000: 0.9,
        3000: 1,
        5000: 1.1,
        10000: 1.3
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



