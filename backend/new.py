from fastapi import FastAPI,HTTPException,Header,Depends
from fastapi.security import HTTPBearer
from pydantic import BaseModel,Field
from slowapi import Limiter, _rate_limit_exceeded_handler
from slowapi.util import get_remote_address
from slowapi.errors import RateLimitExceeded
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
import requests
import uvicorn


### INIT API ###
app = FastAPI()
security = HTTPBearer()
limiter = Limiter(key_func=get_remote_address)
app.state.limiter = limiter
app.add_exception_handler(RateLimitExceeded, _rate_limit_exceeded_handler)



@app.get("/")
async def main():
    return "Ludice API"


def write_deafault_bank(username:str) -> bool:
    try:
        with open("bank.json","r") as file:
            data = json.load(file)
        data.append({
            "username":username,
            "balance":0
        }) 
        with open("bank.json","w") as file:
            json.dump(data,file)
    except Exception as e:
        return False        

def get_ton_url() -> str:
    with open("secrets.json","r") as file:
        data = json.load(file)



def pay() -> bool:
    pass

def write_def_stats(user_id:str) -> bool:
    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        data.append({
            "user_id":user_id,
            "wins":0,
            "total_games":0
        })    
        with open("stats.json","w") as file:
            json.dump(data,file)
        return True    
    except Exception as e:
        return False
    

try:
    redis = redis.Redis('localhost',6379,0,decode_responses=True)
except Exception as e:
    print(f"Redis is not start")    

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


time_lock = threading.Lock()
def check_time_seciruty(username:str) -> bool:
    with time_lock:
        with open("time_sec.json","r") as file:
            data = json.load(file)
        cur_time = time.time()   
        if username in data:
            if cur_time - data[username] < 1:
                return False
        data[username] = cur_time
        #clear all old data

        cleaned_data = {}

        for user,user_time in data.items():
            if cur_time - user_time < 3600:
                cleaned_data[user] = user_time
        with open("time_sec.json","w") as file:
            json.dump(data,file)
        return True
                

class Register(BaseModel):
    username:str# передавай id юзера
    psw:str# это бялть зачем здесь?
    psw:str
    signature:str
    timestamp:float = Field(default_factory=time.time)

def redis_register(username:str,pasw:str) -> bool:
    if redis.exists(f"user:{username}"):
        return False
    else:
        redis.set(f"user:{username}",pasw)
        return True
    


@app.post("/register")

async def register(request:Register):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    if not verify_signature(request.dict(),request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")
    with open("data/users.json","r") as file:
        data = json.load(file)
    if request.username in data:
        raise HTTPException(status_code=400,detail="User already exists")
    else:
        write_deafault_bank(request.username)
        data[request.username] = request.psw
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



class IncreaseUserBalance(BaseModel):
    username:str
    amount:int
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/user/increase")
async def increase_user_balance(request:IncreaseUserBalance):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    try:
        done = False
        with open("bank.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == request.username:
                user["balance"] += request.amount
                with open("bank.json","w") as file:
                    json.dump(data,file)
                done = True
        if not done:
            raise HTTPException(status_code=404,detail="User not found")            

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error something went wrong : {e}")
@app.post("/user/withdraw")
async def withdraw(request:IncreaseUserBalance):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )
    try:
        with open("bank.json","r") as file:
            data = json.load(file)
        done = False
        for user in data:
            if user["username"] == request.username:
                try:
                    if user["balance"] >= request.amount:
                        user["balance"] -= request.amount
                        with open("bank.json","w") as file:
                            json.dump(data,file)
                    raise HTTPException(status_code=400,detail=f"User balance doesnt have this much money :(")
                except Exception as e:
                    raise HTTPException(status_code=400,detail=f"Error while withdraw : {e}")    

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Something went wrong : {e}")


@app.get("/get/{username}/balance")
async def get_user_balance(username:str):
    if not check_time_seciruty(username):
        raise HTTPException(status_code=429,detail="Too many requests")
    try:
        with open("bank.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == username:
                try:
                    return user["balance"]
                except Exception as e:
                    raise HTTPException(status_code=400,detail=f"Error while result:{e}")  
        raise HTTPException(status_code=404,detail=f"User:{username} not found")         
            
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")


@app.get("/count_money")
async def count_all_money():
    try:
        with open("bank.json","r") as file:
            data = json.load(file)
        total = 0
        for user in data:
            try:
                total += user["balance"]
            except Exception as e:
                raise HTTPException(status_code=400,detail=f"Error while counting {e}")       
        return total     
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Something went wrong {e}")


class Start_Game(BaseModel):
    username:str
    bet:int
    timestamp: float = Field(default_factory=time.time)
    signature:str

@app.post("/start/game")
async def start_game(request:Start_Game):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
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
            add_game(user_id = request.username)
            add_win(user_id = request.username)
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
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
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
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
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
    if not check_time_seciruty(request.user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
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
    if not check_time_seciruty(request.user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
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
    if not check_time_seciruty(user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
    with open("bank.json","r") as file:
        data = json.load(file)
    balance = None    
    for user in data:
        if user["username"] == user_id:
            balance = user["balance"]


    try:
        with open("stats.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["user_id"] == user_id:
                wins_pocent = count_of_wins(user_id)
                return {
                    "Total games":user["total_games"],
                    "Wins":user["wins"],
                    "Wins procent" : wins_pocent,
                    "Balance":balance
                }
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")        


def is_user_playing(user_id:str) -> bool:
    with open("gane.json","r") as file:
        data = json.load(file)
    for game in data:
        if user_id in game["players"]:
            return True
    return False
        


@app.get("/isuser/playing/{user_id}")
async def is_playing(user_id:str) -> bool:
    if not check_time_seciruty(user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
    try:
       return is_user_playing(user_id)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error {e}")

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
    if not check_time_seciruty(user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
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
# Интрефейс Платежки
class PaymentInter:
    def __init__(self):
        pass
    def create_payment(self):
        pass
    def get_user_balance(self):
        pass


class TelegrammPayment(PaymentInter):
    def __init__(self,bot_token):
        self.token = bot_token
        self.url = f"https://api.telegram.org/bot{bot_token}"    
    def create_payment(self,chat_id:str,description:str,amount:int,title:str):
        payload = {
            "chat_id": chat_id,
            "title": title,
            "description": description,
            "payload": "stars_payment",
            "provider_token": "YOUR_PAYMENT_PROVIDER_TOKEN", 
            "currency": "XTR",  
            "prices": [{"label": "Stars", "amount": amount}] 
        }
        response = requests.post(f"{self.url}/sendInvoice", json=payload)
        return response.json()
    def get_user_balance(self,user_id:str):
        try:
            payload = {"user_id": user_id}
            response = requests.post(f"{self.base_url}/getUserStars", json=payload)
            return response.json()
        except Exception as e:
            return f"Exception {e}"
        


UserPayment = TelegrammPayment("TOKEN")
class Get_User_Balance(BaseModel):
    user_id:str
    signature:str
    timestamp:float = Field(default_factory=time.time)

async def get_user_balance(request:Get_User_Balance):
    if not check_time_seciruty(request.user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )    
    try:
        return UserPayment.get_user_balance(user_id=request.user_id)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Payment Error: {e}")
class Payment(BaseModel):
    user_id:str
    title:str
    description:str
    amount:int
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/user/pay")
async def user_pay(request:Payment):
    if not check_time_seciruty(request.user_id):
        raise HTTPException(status_code=429,detail="Too many requests")
    request_dict = request.dict()
    if not verify_signature(request_dict, request.signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid signature - data tampered"
        )   
    try:
        UserPayment.create_payment(
            chat_id = request.user_id,
            description = request.description,
            amount = request.amount,
            title = request.title,
        )
        return True
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")

def is_game2_already_played_by_user(username:str) -> bool:
    with open("data_second_game.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == username:
            return True
    return False        


############ SECOND GAME ############
####################################
####################################
####################################



class Start_Second_Game(BaseModel):
    username:str
    bet:int
    num:int
    signature:str
    id:str = Field(default_factory=lambda: str(uuid.uuid4()))
    timestamp:float = Field(default_factory = time.time)
@app.post("/start/new/game2")
async def start_new_game(request:Start_Second_Game):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")
    try:
        with open("data_second_game.json","r") as file:
            data = json.load(file)
        id = str(uuid.uuid4())    
        if not is_game2_already_played_by_user(request.username):
            data.append({
                "username":request.username,
                "bet":request.bet,
                "win":False,
                "num":request.num,
                "id":id
            })
            with open("data_second_game.json","w") as file:
                json.dump(data,file)
            return id
        else:
            raise HTTPException(status_code=400,detail="User is already playing")    

    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")    

class Delete_Game(BaseModel):
    usernmae:str
    id:str
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/delete_game")
async def delete_game(request:Delete_Game):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")
    else:
        try:
            with open("data_second_game=.json","r") as file:
                data = json.load(file)
            for game in data:
                if game["username"] == request.usernmae and game["id"] == request.id:
                    index = data.index(game)
                    data.pop(index)
                    with open("data_second_game.json","w") as file:
                        json.dump(data,file)
                    return True
            raise HTTPException(status_code=404,detail="Game not found")            
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Error : {e}")  
class GetUserGuess(BaseModel):
    username:str
    siganture:str
    timestamp : float = Field(default_factory = time.time)
    id:str = Optional[str]
@app.post("/get/user/num")
async def get_user_num(request:GetUserGuess):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    if not verify_signature(request.model_dump(),request.siganture):
        raise HTTPException(status_code=403,detail="Invalid signature")
    else:
        try:
            with open("data_second_game.json","r") as file:
                data = json.load(file)
            if request.id:
                for game in data:
                    if game["id"] == request.id:
                        return game["num"]
            else:
                for game in data:
                    if game["username"] == request.username:
                        return game["num"]
            raise HTTPException(status_code=404,detail="Game not found")                    
        except Exception as e:
            raise HTTPException(status_code=400,detail=f"Error : {e}")           
######### Drotic Game #########
###############################
###############################
class StartnewGame(BaseModel):
    usernmae:str
    bet:int
    signature:str
    timestamp:float = Field(default_factory = time.time)
@app.post("/start/drotic/game")
async def start_drotic_game(request:StartnewGame):
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code = 403,detail = "Invalid signature") 
    else:
        with open("drotic.json","r") as file:
            data = json.load(file)
        found = False    
        for game in data:
            if game["bet"] == request.bet and len(game["players"]) == 1 and request.username not in game["players"]:
                game["players"].append(request.usernmae)
                id = game["id"]
                with open("drotic.json","w") as file:
                    json.dump(data,file)
                found = True    
                return id
        if not found:
            with open("drotic.json","r") as file:
                data = json.load(file)
            for game in data:
                if game["bet"] == request.bet and len(game["players"]) == 0:
                    game["players"].append(request.username)
                    game["bet"] = request.bet
                    id = game["id"]
                    with open("drotic.json","w") as file:
                        json.dump(data,file)
                    raise HTTPException(status_code = 400,detail = f"Lobby not found : {id}")            
                       
class DeleteGame(BaseModel):
    id:str
    signature:str
    timestamp:float = Field(default_factory = time.time) 
@app.post("/delete/drotic/game")
async def delete_drotic_game(request:DeleteGame):
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code = 403,detail = "Invalid Signature")
    else:
        try:
            with open("drotic.json","r") as file:
                data = json.load(file)
            for game in data:
                if data["id"] == request.id:
                    ind = data.index(game)    
                    data.pop(ind)
                    with open("drotic.json","w") as file:
                        json.dump(data,file)
                    return True
            raise HTTPException(status_code = 404,detail = "User not found")        
        except Exception as e:
            raise HTTPException(status_code = 400,detail = f"Error : {e}")           
class WriteOneTry(BaseModel):
    username:str
    result:str
    id:str
    signature:str
    timestamp:float = Field(default_factory = time.time)
@app.post("/write/one/try")
async def write_one_try(request:WriteOneTry):
    if not check_time_seciruty(request.username):
        raise HTTPException(status_code=429,detail="Too many requests")
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code = 403,detail = "Invalid signature")
    else:
        try:
            with open("drotic.json","r") as file:
                data = json.load(file)
            for game in data:
                if game["id"] == request.id:
                    game["cache"].append({
                        "username":request.username,
                        "result":request.result
                    })
                    with open("drotic.json","w") as file:
                        json.dump(data,file)
                    return True
            raise HTTPException(status_code = 404,detail = "User not found")        
        except Exception as e:
            raise HTTPException(status_code = 400,deatail = f"Error : {e}")    
def payment(amount:int,user_id:str) -> bool:
    url = "http://0.0.0.0:8080/user/pay"
    sig= "TEST SIGNATURE"
    try:
        data = {
            "username": user_id,
            "amount": amount,
            "message":""
        }
        data_str = json.dumps(data, sort_keys=True, separators=(',', ':'))
        
        signature = hmac.new(
            sig.encode(),
            data_str.encode(),
            hashlib.sha256
        )
        
        headers ={
            "Content-Type": "application/json",
            "X-Signature": signature.hexdigest()
        }

        response = requests.post(url, headers=headers, json=data)
    except Exception as e:
        raise HTTPException(status_code = 400,detail = "Error")
if __name__ == "__main__":
    uvicorn.run(app,host = "0.0.0.0",port = 8080)
