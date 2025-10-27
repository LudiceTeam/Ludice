#Этот бот будет информировать нас когда у нас на балансе не будет хватать денег
import telebot
import json
from fastapi import FastAPI,HTTPException
from pydantic import BaseModel,Field
import uvicorn
import requests
import hmac
import uuid
import time





def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)

def get_token() -> str:
    with open("secrets.json","r") as file:
        data = json.load(file)
    return data["info_bot"]




TOKEN = get_token()
bot = telebot.TeleBot(TOKEN)
app = FastAPI()
@app.get("/")
async def main():
    return "Notify bot"

@bot.message_handler(commands=["start"])
def start(message):
    bot.send_message(message.chat.id,f"Наш баланс:")




    