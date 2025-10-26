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
import uuid

# МЫ В ПИЗДЕ 
#НАДО ПОЛЬНОСТЬЮ ПЕРЕПИСЫВАТЬ ВСЕ ЭТУ ЕБЕНЬ

cache = {
    "payments":"payments.json",
    "api_token":"some_token",
    "url":"some_url",
    "key":"some_key",
    "ton_wallet":"key"
}
PROVIDER  = "SOME PROVIDER" # Fragment
PROVIDER_KEY  = "YOUR_PROVIDER_API_KEY"   


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


def count_commission(amount:int) -> int:
    return math.floor(amount * 0.7) #Если нужно поменяй на другой процент 

def create_fragment_order(to_user:str,amount:int,message:str = ""):
    headers = {"Authorization": f"Bearer {PROVIDER_KEY}", "Content-Type": "application/json"}
    payload = {"user_id": to_user, "amount_xtr": amount, "note": message}
    r = req.post(f"{PROVIDER}/orders", headers=headers, json=payload, timeout=30)
    r.raise_for_status()
    return r.json()


def get_order_status(order_id:str):
    headers = {"Authorization": f"Bearer {PROVIDER_KEY}"}
    r = req.get(f"{PROVIDER}/orders/{order_id}", headers=headers, timeout=20)
    r.raise_for_status()

#history of the payments
def write_payment(payment:list[str]):
    try:
        with open("data/payments.json","r") as file:
            data = json.load(file)
        data.append({
            "id":uuid.uuid4(),
            "time":time.time(),
            "info":payment
        })    
        with open("data/secrets.json","w") as file:
            json.dump(data,file)
    except Exception as e:
        print(f"Error : {e}")
app = FastAPI()
@app.get("/")
async def main():
    return "Finance API"



mnemo = [
        "слово1", "слово2", "слово3", "слово4", "слово5", "слово6",
        "слово7", "слово8", "слово9", "слово10", "слово11", "слово12",
        "слово13", "слово14", "слово15", "слово16", "слово17", "слово18",
        "слово19", "слово20", "слово21", "слово22", "слово23", "слово24"
    ]
to_addr = "EQD...адрес_провайдера..."
payer = TonPayer(mnemo)
payer.init()

class Payment(BaseModel):
    to:str
    amount:str
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/pay")
async def pay(request:Payment):
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=429,detail = "Invalid signature")
    else:
        #create an order to fragment
        #Тут создаеться заказ (так работает Fragment)
        order = create_fragment_order(request.to,count_commission(request.amount),"Your win. Play Ludice")
        write_payment([order["id"]],order["status"],order["amount_nano"],request.to)
        nano = int(request.amount * NANOTON)
        try:
            #Вот тут мы платим TON фрагменту
            result = payer.pay_ton(order["ton_address"],order["amount_nano"],"Your win. Play Ludice")
        except Exception as e:
            print(f"Error : {e}")

if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0",port = 8080)         