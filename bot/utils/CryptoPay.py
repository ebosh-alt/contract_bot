import asyncio

import requests
from aiocryptopay import AioCryptoPay, Networks
from aiocryptopay.models.currencies import Currency

networks = {
    "test": Networks.TEST_NET,
    "main": Networks.MAIN_NET}


class CryptoPay:
    def __init__(self, api_key: str, network: str = "test"):
        self.crypto = AioCryptoPay(token=api_key, network=networks.get(network))

    async def profile(self):
        return await self.crypto.get_me()

    async def currencies(self) -> list[Currency]:
        return await self.crypto.get_currencies()

    async def create_invoice(self, asset: str, amount: float):
        invoice = await self.crypto.create_invoice(asset=asset, amount=amount)
        return invoice

    async def get_invoice(self, invoice_ids: int):
        invoices = await self.crypto.get_invoices(invoice_ids=invoice_ids)
        return invoices

    async def close_session(self) -> None:
        await self.crypto.close()



if __name__ == "__main__":
    pay = CryptoPay("7290:AAIpTLty9MMYPKFvlOxDkD3Ob0VTBl9fD2H")
    print(pay.get_invoice(1))
