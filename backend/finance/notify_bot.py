#Этот бот будет информировать нас когда у нас на балансе не будет хватать денег
import telebot
import json
from fastapi import FastAPI,HTTPException,Request,Depends
from pydantic import BaseModel,Field
import uvicorn
import requests
import hmac
import uuid
import time
import hashlib
import threading
from secrets import compare_digest



def get_siganture_key() -> str:
    try:
        with open("secrets.json","r") as file:
            data  = json.load(file)
        return data["key"]    
    except Exception as e:
        print(f"Error : {e}")
        raise KeyError("Error")


def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    KEY = get_siganture_key()
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)
def get_balance():
    try:
        url = "http://0.0.0.0:8080/get/wallet/balance"
        req = requests.get(url)
        print(f"STATUS CODE : {req.status_code}")
        print(f"TEXT : {req.text}")
        print(f"JSON : {req.json()}")
        return req.json()
    except Exception as e:
        print(f"Exception as {e}")    

def get_api_key():
    with open("data/secrest.json","r") as file:
        data = json.load(file)
    return data["api_key"]        

async def require_api_header(req:Request):
    api = req.headers.get("X-API-Key")
    if not api or not compare_digest(api,get_api_key()):
        raise HTTPException(status_code=401,details = "Invalid api key")        

def get_token() -> str:
    with open("secrets.json","r") as file:
        data = json.load(file)
    return data["info_bot"]

def get_all_user_balances():
    url = "http://0.0.0.0:8080/count_money"
    try:
        req = requests.get(url)
        print(f"STATUS CODE : {req.status_code}")
        print(f"TEXT : {req.text}")
        print(f"JSON : {req.json()}")
        return req.json()
    except Exception as e:
        print(f"Exception : {e}")
     

#----- INIT -----
TOKEN = get_token()
bot = telebot.TeleBot(TOKEN)
app = FastAPI()



@app.get("/")
async def main():
    return "Notify bot"

chat_id_text = None
@bot.message_handler(commands=["start"])
def start(message):
    chat_id_text = message.chat.id
    balance = get_balance()
    bot.send_message(message.chat.id,f"Наш баланс: {balance}")
    user_balances = get_all_user_balances()
    bot.send_message(message.chat.id,f"Все деньги в обороте : {user_balances}")

class Notify(BaseModel):
    siganture:str
@app.get("/notify",dependencies=[Depends(require_api_header)])
async def notify(request:Notify):
    try:
        if chat_id_text is not None:
            bot.send_message(chat_id_text,"НА СЧЕТУ НЕ ХВАТАЕТ TON")
        else:
            raise HTTPException(status_code  = 400,detail="Error : no chat id")   
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")

def run_bot():
    bot.polling(none_stop=True)
def run_api():
    uvicorn.run(app,host="0.0.0.0",port = 1488)
if __name__ == "__main__":
    threading.Thread(target=run_bot,daemon=True).start()
    run_api()

    