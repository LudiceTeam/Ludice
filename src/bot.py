from pathlib import   Path
from dotenv import  load_dotenv
import os

ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

TOKEN = (
    os.getenv("TELEGRAM_BOT_TOKEN")
)

if not TOKEN:
    print("Missing token")
else:
    print("Token found")

import asyncio
import logging
import sys
from os import getenv



from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
import requests

from handlers import start, help 

API_TOKEN = "YOUR_TOKEN_HERE"

def send_user_to_api(username, user_id):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id": user_id
    }
    resp = requests.post(url, json=data)
    return resp.status_code == 200

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if send_user_to_api(username, user_id):
        await message.reply("You have been registered successfully!")
    else:
        await message.reply("Registration failed. Please try again later.")


if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


