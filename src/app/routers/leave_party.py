# /leave_party game (command handler)
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

from app.states import CreatePaerty
from app.keyboards import game_type_kb

router = Router()

logging.basicConfig(level=logging.INFO)