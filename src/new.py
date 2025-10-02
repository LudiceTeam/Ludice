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
import time




def write_def_stats(user_id:str) -> bool:
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        data.append({
            "user_id":user_id,
            "wins":0,
            "total_games":0
        })    
        with open("stats.json","r") as file:
            json.dump(data,file)
        return True    
    except Exception as e:
        return False


redis = redis.Redis('localhost',6379,0,decode_responses=True)

app = FastAPI()



@app.get("/")
async def main():
    return "Ludice API"




class Register(BaseModel):
    username:str# передавай id юзера
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
            write_def_stats(request.username)    

def get_key() -> str:
    with open("secrets.json","r") as file:
        data = json.load(file)
    return data["key"]    

KEY = get_key()


def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)


def delete_the_same(bet:int,user_id1 : str,user_id2:str,id_that_we_need:str) -> bool:
    with open("game.json","r") as file:
        data = json.load(file)
    for game in data:
        if game["id"] != id_that_we_need and user_id1 in data["players"] and user_id2 in data["players"] and game["bet"] == bet:
            ind = data.index(game)
            data.pop(ind)
            with open("game.json","w") as file:
                json.dump(data,file)
            return True
    return False        



class Start_Game(BaseModel):
    username:str
    bet:int
    timestamp: float = Field(default_factory=time.time)
    signature:str

@app.post("/start/game")
async def start_game(request:Start_Game):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    found = False
    with open("game.json","r") as file:
        data = json.load(file)
    found_id = ""    
    for game in data:
        if len(game["players"]) == 1 and game["bet"] == request.bet and request.username not in game["players"]:
            game["players"].append(request.username)
            found = True
            found_id = game["id"]
    if found:
        with open("game.json","w") as file:
            json.dump(data,file)
        return found_id
    else:
        for game in data:
            if len(game["players"]) == 0:
                game["bet"] = request.bet  
                game["players"].append(request.username)
                with open("game.json","w") as file:
                    json.dump(data,file)
                raise HTTPException(status_code=400,detail=game["id"])
def add_win(user_id:str) -> bool:
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["user_id"] == user_id:
                user["wins"] += 1
                with open("stats.json","w") as file:
                    json.dump(data,file)
                return True         
        return False
    except Exception as e:
        return False
def add_game(user_id:str) -> bool:
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["user_id"] == user_id:
                user["total_games"] += 1
                with open("stats.json","w") as file:
                    json.dump(data,file)     
                return True
        return False     
    except Exception as e:
        return False  
def count_procent_of_wins(user_id:str) -> float:
    try:
        found = False
        with open("stats.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["user_id"] == user_id:
                found = True
                return float(user["total_games"] / user["wins"]) * 100
        if found:
            return True
        return False                    
                 
    except Exception as e:
        raise e        

class Cancel_My_Find(BaseModel):
    username:str
    id:str
    signature:str
    timestamp: float = Field(default_factory=time.time)
@app.post("/cancel/find")
async def cancel_find(request:Cancel_My_Find):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    with open("game.json","r") as file:
        data = json.load(file)               
    try:
        for game in data:
            if game["id"] == request.id and len(game["players"]) == 1 and request.username in game["players"]:
                ind = data.index(game)
                data.pop(ind)
                with open("game.json","w") as file:
                    json.dump(data,file)
                return True
        return False             
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Exception as {e}")         



class Win(BaseModel):
    username:str
    id:str
    signature:str
    timestamp: float = Field(default_factory=time.time)
@app.post("/write/winner")
async def write_winner(request:Win):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    try:
        with open("game.json","r") as file:
            data = json.load(file)
        for game in data:
            if game["id"] == request.id and len(game["players"]) == 2 and request.username in game["players"]:
                if game["winner"] == "":
                    game["winner"] = request.username
                    with open("game.json","w") as file:
                        json.dump(data,file)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error {e}")   

class Leave(BaseModel):
    user_id:str
    id:str
    signature:str
    timestamp: float = Field(default_factory=time.time)
@app.post("/leave")
async def leave(request:Leave):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    try:
        with open("game.json","r") as file:
            data = json.load(file)
        for game in data:
            if game["id"] == request.id:
                if len(game["players"]) == 2 and request.user_id in game["players"]:
                    game["players"] = []
                    game["bet"] = 0
                    game["winner"] = ""
                    with open("game.json","w") as file:
                        json.dump(data,file)
                    return True
        raise HTTPException(status_code=400,detail="Error lobby not found :(")        
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error: {e}")    

class Procent_Of_Wins(BaseModel):
    user_id:str
    signature:str
    timestamp: float = Field(default_factory=time.time)
@app.post("/count/wins") 
async def count_of_wins(request:Procent_Of_Wins):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    result = count_of_wins(request.user_id)
    try:
        return result
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error: {e}")    
@app.get("/get/leader/board/most_games")
async def get_leader_board_games():
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        result = {}
        for user in data:
            result[user["user_id"]] = user["total_games"]   
        return result     
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error: {e}")
@app.get("/get/procent/wins")
async def get_leader_board():
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        result = {}
        for user in data:
            pr = count_of_wins(user["user_id"])
            result[user["user_id"]] = pr
        return result        
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error:{e}")

@app.get("/getme/{user_id}")
async def get_me(user_id:str):
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["user_id"] == user_id:
                wins_pocent = count_of_wins(user_id)
                return {
                    "Total games":user["total_games"],
                    "Wins":user["wins"],
                    "Wins procent" : wins_pocent
                }
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")        


def is_user_playing(user_id:str):
    pass


@app.get("/isuser/playing/{user_id}")
async def is_playing(user_id:str) -> bool:
    pass

class WriteRes(BaseModel):
    user_id:str
    game_id:str
    result:int
    signature:str
    timestamp: float = Field(default_factory=time.time)
@app.post("/write/res")
async def write_res(request:WriteRes):
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    try:
        with open("game.json","r") as file:
            data = json.load(file)
        for game in data:
            if game["id"] == request.game_id:
                if len(game["players"]) == 2 and request.user_id in game["players"]:
                    game[f"result_{request.user_id}"] = request.result
                    with open("game.json","w") as file:
                        json.dump(data,file)
                    return True
        return False         
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")        
        



@app.get("/join/link/{game_id}/{user_id}/{bet}")
async def join_by_the_link(user_id:str,bet:int,game_id:str):
    try:
        with open("game.json","r") as file:
            data = json.load(file)
        done = False
        for game in data:
            if game["id"] == game_id:
                try:
                    if len(game["players"] == 1 and user_id not in game["players"]) and game["bet"] == bet:
                        game["players"].append(user_id)
                        done = True
                        with open("game.json","w") as file:
                            json.dump(data,file)
                        return True
                    else:
                        raise HTTPException(status_code=400,detail="Lobby is full")
                     
                except Exception as e:
                    raise HTTPException(status_code=400,detail=f"Error : {e}")        

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error while joining : {e}")


