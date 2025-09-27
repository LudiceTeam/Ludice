# /rgame or random game (command handler)
from aigoram import router 
from random import choice
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext
import logging

from app.states import CreatePaerty
from app.keyboards import game_type_kb

logging.basicConfig(level=logging.INFO)
router = Router()