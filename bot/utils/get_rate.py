from datetime import datetime

from pycbrf.toolbox import ExchangeRates


def get_rate():
    date = datetime.now()
    rates = ExchangeRates(date)
    return rates["USD"].value
