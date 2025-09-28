# /delete_party (command handler)
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

def send_user_to_api(username, id, title, is_open=True):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id": id,
    }
    # Done send request to API
    resp = requests.post(url, json=data)
    return resp.status_code == 200
