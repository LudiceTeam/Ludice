# # /create_party (command handler)
# import logging
# from aiogram import Router
# from aiogram.filters import Command
# from aiogram.types import Message
# from aiogram.fsm.context import FSMContext
# import requests

# from app.states import CreatePaerty
# from app.keyboards import game_type_kb

# router = Router()

# logging.basicConfig(level=logging.INFO)

# def send_user_to_api(username, id, title, is_open=True):
#     url = "http://0.0.0.0:8000/register"
#     data = {
#         "username": username,
#         "id": id,
#         "title": title,
#         "is_open": is_open
#     }
#     # Done send request to API
#     resp = requests.post(url, json=data)
#     return resp.status_code == 200

# @router.message(Command("create_party"))
# async def cmd_start(message: Message, state: FSMContext):
#     await state.clear()
#     await message.answer("Hello! Let's create a new party. Please name your party:")
#     await state.set_state(CreateParty.waiting_for_name)

# @router.message(CreateParty.waiting_for_name)
# async def process_game_name(message: Message, state: FSMContext):
#     game_name = message.text
#     if not game_name or len(game_name) > 50:
#         await message.answer("Invalid game name. Please try again.")
#         return
    
#     await state.update_data(game_name=game_name)
#     await message.answer("How many players do you want in your party? (2-10)")
#     number_players = message.text
#     if not number_players.isdigit() or not (2 <= int(number_players) <= 10):
#         await message.answer("Invalid number of players. Please enter a number between 2 and 10.")
#         return
    
#     await state.update_data(number_players=number_players)
#     player_data = await state.get_data(int(number_players))
#     await message.answer("Game has been created successfully!", "Number of players: {number_players}, Game name: {game_name}".format(**player_data))
#     await state.clear() 

#     success = send_user_to_api(
#         username=message.from_user.username, 
#         user_id=message.from_user.id,
#         party_name=game_name,
#         number_of_players=number_players
#     )
