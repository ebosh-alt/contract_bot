import requests


def get_price_coin(name: str):
    url = 'https://pro-api.coinmarketcap.com/v1/cryptocurrency/listings/latest'
    headers = {
        'Accepts': 'application/json',
        'X-CMC_PRO_API_KEY': '5a7a63d0-48b9-4b20-8ec9-d22fa6d2ff8d',
    }
    data = requests.get(url, headers=headers).json()["data"]
    for el in data:
        if el["name"] == name:
            return el["quote"]["USD"]["price"]
