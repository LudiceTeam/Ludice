from fastapi import FastAPI,HTTPException
from pydantic import BaseModel
from pydantic import BaseModel,Field
import json
import threading
import socket
from typing import Union,Literal,List,Optional
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




#Connecting REDIS
class RedisAuth:
    def __init__(self, host='localhost', port=6379, db=0):
        self.redis = redis.Redis(host=host, port=port, db=db, decode_responses=True)
    
    def _hash_password(self, password):
        """Хеширование пароля"""
        return hashlib.sha256(password.encode()).hexdigest()
    
    def _generate_token(self):
        """Генерация токена"""
        return secrets.token_hex(32)


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


                  
@app.post("/login")
async def login(request:Register):
    if redis.exists(f"user:{request.username}"):
        password = redis.get(f"user:{request.username}")
        return password == request.password


class CreateLobby(BaseModel):
    username:str
    title:str
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))

@app.post("/create/lobby")
async def create_lobby(request:CreateLobby):
    with open("lobby.json","r") as file:
        data = json.load(file)   
    for user in data:  
        if user["username"] == request.username:
            user["lobbys"].append({
                "host":request.username,
                "title":request.title,
                "id":request.id,
                "players":[request.username],
                "bets":[]
            })
            with open("lobby.json","w") as file:
                json.dump(data,file)
            return
    raise HTTPException(status_code=400,detail="User not found")          

class DeleteGame:
    username:str
    id:str

@app.delete("/delete/game")
async def delete_game(request:DeleteGame):
    try:
        with open("lobby.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == request.username:
                for lob in user["lobbys"]:
                    if lob["id"] == request.id:
                        ind = user["lobbys"].index(lob)
                        user["lobbys"].pop(ind)
                        with open("lobby.json","w") as file:
                            json.dump(data,file)
                            return
        raise HTTPException(status_code=400,detail="Bad Request")          
    except Exception as e:
        raise HTTPException(status_code=403,detail=f"Exception : {e}")         

class Bet(BaseModel):
    username:str
    author:str
    id_game:str
    bet:int
    bet_id:str = Field(default_factory=lambda: str(uuid.uuid4()))  
     

@app.post("/bet")
async def bet(request:Bet):
    with open("lobby.json","r") as file:
        data = json.load(file)

    try:
        for user in data:
            if user["username"] == request.author:
                for lob in user["lobbys"]:
                    if lob["id"] == request.id_game:
                        lob["bets"].append({
                            "username":request.username,
                            "bet":request.bet,
                            "bet_id":request.bet_id
                        })
                        with open("lobby.json","w") as file:
                            json.dump(data,file)
                        return    
        raise HTTPException(status_code=400,detail="Lobby not found")            
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error while betting : {e}")
                    

class Cancel_Bet(BaseModel):
    author:str
    id_game:str
    id_bet:str
    author:str

@app.delete("/delete/bet")
async def delete_bet(request:Cancel_Bet):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lob in user["lobbys"]:
                if lob["id"] == request.id_game:
                    for bet in lob["bets"] :
                        if bet["bet_id"] == request.id_bet:
                            ind = lob["bets"].index(bet)
                            lob["bets"].pop(ind)
                            with open("lobby.json","w") as file:
                                json.dumo(data,file)
                            return
    raise HTTPException(status_code=400,detail="Game not found or bet not found")            
#FIXME code an endpoint for  bool is everyone betted
class IsBetted(BaseModel):
    author:str
    lobby_id:str
@app.post("/isbetted")
async def isbetted(request:IsBetted):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lobby in user["lobbys"]:
                if lobby["id"] == request.lobby_id:
                    return len(lobby["bets"]) == len("players")
    raise HTTPException(status_code=400,detail="Wrong data")                