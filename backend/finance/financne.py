import requests as req
import json
from pydantic import Field,BaseModel
from fastapi import FastAPI,HTTPException,Header
import time 
import hmac
import hashlib
import uvicorn
import math
import asyncio
from ton import Tonlib, Wallet

# МЫ В ПИЗДЕ 
#НАДО ПОЛЬНОСТЬЮ ПЕРЕПИСЫВАТЬ ВСЕ ЭТУ ЕБЕНЬ

cache = {
    "payments":"payments.json",
    "api_token":"some_token",
    "url":"some_url",
    "key":"some_key",
    "ton_wallet":"key"
}


KEY = ""
def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)


NANOTON = 10**9

class TonPayer:
    def __init__(self, mnemonics: list[str]):
        self.mnemonics = mnemonics
        self.ton = Tonlib()
        self._wallet = None

    def init(self):
        # Если библиотека Tonlib требует инициализацию
        if hasattr(self.ton, "init"):
            self.ton.init()
        self._wallet = Wallet.from_mnemonics(self.ton, self.mnemonics)

    def close(self):
        if hasattr(self.ton, "close"):
            self.ton.close()

    def pay_ton(self, to_address: str, amount_nano: int, comment: str = ""):
        """
        Синхронно отправляет amount_nano TON на указанный адрес.
        Возвращает dict с результатом транзакции.
        """
        # 1. Проверяем баланс
        balance = self._wallet.get_balance()
        fee_reserve = int(0.05 * NANOTON)  # запас на комиссию
        if balance < amount_nano + fee_reserve:
            raise RuntimeError(
                f"Недостаточно TON: нужно {(amount_nano + fee_reserve)/NANOTON:.3f}, "
                f"есть {balance/NANOTON:.3f}"
            )

        # 2. Отправляем транзакцию
        tx_info = self._wallet.transfer(
            to_address=to_address,
            amount=amount_nano,
            comment=comment
        )

        return tx_info




app = FastAPI()
@app.get("/")
async def main():
    return "Finance API"



if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0",port = 8080)         