#python imports
import asyncio
import os

# framework imports
from aiogram import Bot, Dispatcher, types
from aiogram.filters import CommandStart

# env imports
from dotenv import load_dotenv, find_dotenv 
load_dotenv(find_dotenv())

# project imports
from routers.start import start_router

ALLOWED_UPDATES = ["message", "edited_message", "callback_query"]

bot = Bot(token=os.getenv("TOKEN"))
dp = Dispatcher()

dp.include_router(start_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True) 
    await dp.start_polling(bot, allowed_updates=ALLOWED_UPDATES)
asyncio.run(main())