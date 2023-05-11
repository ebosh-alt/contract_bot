from yookassa import Payment, Configuration

# Configuration.account_id = '980889'
# Configuration.secret_key = 'live_JB-sjh_-FPp_2Rl5QeX5Rlm6lwqarahXnk4YAbZCOnQ'


def check_pay(key: str):
    try:
        res = Payment.find_one(key)
        if res.paid and res.status == "succeeded":
            return res
        else:
            return False
    except:
        return False
