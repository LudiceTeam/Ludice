from pathlib import   Path
from dotenv import  load_dotenv
import os
import sys
from os import getenv
from aiogram import Bot, Dispatcher, executor, types
import asyncio
import logging
import requests
from handlers import start, help
 
ROOT = Path(__file__).resolve().parents[1]
ENV_PATH = ROOT / ".env"
load_dotenv(dotenv_path=ENV_PATH)

TOKEN = (
    os.getenv("TELEGRAM_BOT_TOKEN")
)

if not TOKEN:
    print("Missing token")
else:
    print("Token found")

API_TOKEN = "YOUR_TOKEN_HERE"

def send_user_to_api(username, user_id):
    url = "http://0.0.0.0:8000/register"
    data = {
        "username": username,
        "id": user_id
    }
    resp = requests.post(url, json=data)
    return resp.status_code == 200

@dp.message_handler(commands=['start'])
async def start(message: types.Message):
    user_id = message.from_user.id
    username = message.from_user.username
    if send_user_to_api(username, user_id):
        await message.reply("You have been registered successfully!")
    else:
        await message.reply("Registration failed. Please try again later.")

@dp.message_handler(commands=['lobby'])
async def lobby(message: types.Message):
    await message.reply("Welcome to the lobby! Here you can find other players to join your game. \nUse /join <game_id> to join a game. /create and than <game_name> to create a new game.")

@dp.message_handler(commands=['create'])
async def create_game(message: types.Message, state: FSMContext):
    await message.answer("Name your game:")
    await state.set_state(CreateGame.waiting_for_name)

@dp.message_handler(state=CreateGame.waiting_for_name)
async def process_game_name(message: types.Message, state: FSMContext):
    game_name = message.text
    await message.answer(f"Game '{game_name}' created successfully!")
    await state.finish()

@dp.message_handler(commands=['join'])
async def join_game(message: types.Message):
    await message.answer("Enter the game ID you want to join:")
    await state.set_state(JoinGame.waiting_for_game_id) 

@dp.message_handler(state=JoinGame.waiting_for_game_id)
async def process_game_id(message: types.Message, state: FSMContext):
    game_id = message.text
    await message.answer(f"You have joined the game with ID: {game_id}")
    await state.finish()

if __name__ == "__main__":
    executor.start_polling(dp, skip_updates=True)


