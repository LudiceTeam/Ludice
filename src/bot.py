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



from aiogram import Bot, Dispatcher, html
from aiogram.client.default import DefaultBotProperties
from aiogram.enums import ParseMode
from aiogram.filters import CommandStart
from aiogram.types import Message

bot = Bot(token=TOKEN, default=DefaultBotProperties(parse_mode=ParseMode.HTML))
dp = Dispatcher()



