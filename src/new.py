from fastapi import FastAPI,HTTPException,Header
from pydantic import BaseModel
from pydantic import BaseModel,Field
import json
import threading
import socket
from typing import Union,Literal,List,Optional,Any
import random
from pydantic.types import StrictStr
from pydantic_core.core_schema import str_schema
import uuid
import redis
import secrets
import hashlib
from jose import JWTError
import jwt
from passlib.context import CryptContext
from filelock import FileLock
import hmac
import secrets



redis = redis.Redis('localhost',6379,0,decode_responses=True)


app = FastAPI()
@app.get("/")


async def main():
    return "Ludice API"


class Register(BaseModel):
    username:str
    id:str

@app.post("/register")
async def register(request:Register):
    if redis.exists(f"user:{request.username}"):
        raise HTTPException(status_code=400,detail="User already exists")
    else:
        redis.set(f"user:{request.username}",request.id)
        with open("data/users.json","r") as file:
            data = json.load(file)
        if request.username in data:
            raise HTTPException(status_code=400,detail="User alredy exists")
        else:
            data[request.username] = request.id
            with open("data/users.json","w") as file:
                json.dump(data,file)  
            # DEFAULT LOBBY DATA
            with open("lobby.json","r") as file:
                lobs = json.load(file)
            lobs.append({
                "username":request.username,
                "lobbys":[]
            })
            with open("lobby.json","w") as file:
                json.dump(lobs,file)

class StartGame(BaseModel):
    bet:int
    user_id:str
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))
@app.post("/start/game")
async def start_game(request:StartGame):
    with open("best.json","r") as file:
        data = json.load(file)
    if request.user_id  in data:
        raise HTTPException(status_code=400,detail="You alredy betted")   
    same_bets = {}  
    for user, bet in data.items():
        if bet == request.bet:
            same_bets[user] = bet
    if len(same_bets) != 0:        
        rand_user = random.choice(same_bets.keys())
        rand_bet = same_bets[rand_user]  


    with open("game.json","r") as file:
        games = json.load(file)

    games.append(
        {
            "id":str(uuid.uuid4()),
            "players":[request.user_id,rand_user]
        }
    )    
                 




        


            