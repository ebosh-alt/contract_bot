from yookassa import Payment, Configuration

from bot.config import link_to_bot

Configuration.account_id = '873492'
Configuration.secret_key = 'test_rFwIwdtgIwpyQgI555vYUd7u_Nd8p3u2A2h5o5diF0Q'


def create_pay(user_id: str, price: float) -> tuple:
    Configuration.account_id = '873492'
    Configuration.secret_key = 'test_rFwIwdtgIwpyQgI555vYUd7u_Nd8p3u2A2h5o5diF0Q'
    payment = Payment.create({
        "amount": {
            "value": price,
            "currency": "RUB"
        },
        "confirmation": {
            "type": "redirect",
            "return_url": link_to_bot

        },
        "capture": True,
        "description": user_id,
        "receipt": {"customer": {"email": "isakovn2005@gmail.com"}}
    })
    return payment.confirmation.confirmation_url, payment.id


if __name__ == "__main__":
    print(create_pay("55", 76820.7))
