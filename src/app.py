import asyncio
import os
from aiogram import Bot, Dispatcher
from dotenv import load_dotenv, find_dotenv


load_dotenv(find_dotenv())
TOKEN = os.getenv("TOKEN")

from routers.private_user import start_router

bot = Bot(TOKEN)
dp = Dispatcher()
dp.include_router(start_router)

async def main():
    await bot.delete_webhook(drop_pending_updates=True)

    print("✅ Bot started! Waiting for updates...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
