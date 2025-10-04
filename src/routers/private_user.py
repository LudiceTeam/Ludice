from aiogram import F,Router, types
from aiogram.filters import CommandStart, or_f

from keyboard import reply

start_router = Router()


@start_router.message(CommandStart())
async def cmd_start(message: types.Message):
    await message.answer("Welcome to the ludicé bot. Choose an option:", reply_markup=reply.start_kb)

@start_router.message(F.text == "Statictic 📊")
async def about_cmd(message: types.Message):
    await message.answer(
        "Open source project was created by enthusiasts.\n"
        "<a href='https://github.com/DeepBlackHole'>GitHub Repository</a>",
        parse_mode="HTML", reply_markup=reply.del_keyboard,statictic_kb)