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
    user_balance:str
@app.post("/start/game")
async def start_game(request:StartGame):
    with open("bets.json","r") as file:
        data = json.load(file)
    if request.user_id  in data:
        raise HTTPException(status_code=400,detail="You alredy betted")   
    else:
        data[request.user_id] = request.bet
        with open("bets.json","w") as file:
            json.dump(data,file)


        with open("bets.json","r") as file:
            data = json.load(file)    

        opponet = ""
        opponets_bet = 0
        found = False
        for user, bet in data.items():
            if bet == request.bet and user != request.user_id:
                opponet = user
                opponets_bet = bet
                found = True
                break
        if found:
            del data[opponet]
            del data[request.user_id] 
            with open("bets.json","w") as file:
                json.dump(data,file)


            with open("game.json","r") as file:
                games = json.load(file)

            games.append(
                {
                    "id":str(uuid.uuid4()),
                    "players":[request.user_id,opponet],
                    request.user_id : request.bet,
                    opponet:opponets_bet,
                    f"res_{request.user_id}" : 0,
                    f"res_{opponet}" : 0
                }
            )        
            with open("games.json","w") as file:
                json.dump(games,file)

        else:
            del data[request.user_id]
            with open("bets.json","w") as file:
                json.dump(data,file)
            raise HTTPException(status_code=404,detail="Opponent wasnt found")    
        


        
                    




        


            