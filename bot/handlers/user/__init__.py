from .greeding import start_router
from .main_menu import main_router
from .back import back_router
from .refferal import referral_router
from .amount_deposit import amount_deposit_router
from .replenishment import replenishment_router
from .promocode import promocode_router
from .delete_notification import delete_notification_router
from .withdrawal import withdrawal_router
from .ymoney import ymoney_router
from .crypto_payment import crypto_router

user_routers = (start_router, main_router, back_router, referral_router, amount_deposit_router, replenishment_router,
                promocode_router, delete_notification_router, withdrawal_router, ymoney_router, crypto_router)
