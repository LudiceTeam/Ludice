# /join game (command handler)
import logging
from aiogram import Router
from aiogram.filters import Command
from aiogram.types import Message
from aiogram.fsm.context import FSMContext

import requests
from app.states import CreatePaerty
from app.keyboards import game_type_kb

router = Router()

logging.basicConfig(level=logging.INFO)

def join_party(id_game, username, author):
    url = "http://0.0.0.0:8000/join"
    data = {
        "id_game": id_game,
        "username": username,
        "author": author
    }
    # Done request to API
    resp = requests.post(url, json=data)
    return resp.status_code == 200