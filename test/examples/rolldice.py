import asyncio
from aiogram import Bot, Dispatcher, types
from aiogram.filters import Command

API_TOKEN = ("<API_TOKEN>")

bot = Bot(token=API_TOKEN)
dp = Dispatcher()

@dp.message(lambda msg: msg.dice)
async def dice_handler(message: types.Message):
    value = message.dice.value
    await message.answer(f"Value: {value}")

async def main():
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())
