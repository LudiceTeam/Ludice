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
@app.post("/login")
async def login(request:Register):
    if redis.exists(f"user:{request.username}"):
        password = redis.get(f"user:{request.username}")
        return password == request.password


class CreateLobby(BaseModel):
    username:str
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))

@app.get("/create/lobby")
async def create_lobby(request:CreateLobby):
    with open("lobby.json","r") as file:
        data = json.load(file)   
    for user in data:  
        if user["username"] == request.username:
            user["lobbys"].append({
                "host":request.username,
                "id":request.id,
                "players":[request.username],
                "bets":{}
            })
            with open("lobby.json","w") as file:
                json.dump(data,file)
            return
    raise HTTPException(status_code=400,detail="User not found")          

