# /create_party (command handler)
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

def send_user_to_api(username, author, id_game, bet_id, ):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id_game": id_game,
        "author": author,
        "title": title,
        "is_open": is_open,
        "bet": bet
    }
    resp = requests.post(url, json=data)
    return resp.status_code == 200
