from aiogram import F,Router, types
from aiogram.types import LabeledPrice, PreCheckoutQuery, InlineKeyboardMarkup, InlineKeyboardButton
from aiogram.filters import CommandStart
from keyboard import start
from dotenv import load_dotenv, find_dotenv
from aiogram import Bot, Dispatcher, types, F
from aiogram.fsm.state import State, StatesGroup
from aiogram.fsm.context import FSMContext
from aiogram.types import Message
from aiogram.enums import ParseMode
from aiogram.filters import Command
import os

# Load environment variables
load_dotenv(find_dotenv())
ADMIN_PASSWORD = os.getenv("ADMIN_PASSWORD")
ADMIN_KEY = os.getenv("ADMIN_KEY")

# Routers
admin_router = Router()

@admin_router.message(F.text == ADMIN_PASSWORD)
async def admin_access(message: types.Message):
    await message.answer("Admin access granted. Please use the admin key to proceed.")