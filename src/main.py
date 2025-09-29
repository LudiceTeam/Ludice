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
    is_open:bool

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
                "bets":[],
                "open":request.is_open,
                "winner":""
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

SYSTEM_SECRET = "your-super-secret-system-key-12345" 
def create_signature(data:str,secret:str) -> str:
    return hmac.new(
        secret.encode(), 
        data.encode(), 
        hashlib.sha256
    ).hexdigest()

def verify_token(request:Any,role:str,token:str = Header(...)) -> bool:
    data_str = json.dumps(request.dict(), sort_keys=True)
    expected_signature = create_signature(data_str, SYSTEM_SECRET)
    return hmac.compare_digest(token, expected_signature)



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
                    return len(lobby["players"] == len(lobby["bets"].keys()))
    raise HTTPException(status_code=400,detail="Wrong data")


class IsUserBetted(BaseModel):
    author:str
    lobby_id:str
    username:str
@app.post("/check/betted")
async def is_user_betted(request:IsUserBetted) -> bool:
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lob in user["lobbys"]:
                if lob["id"] == request.lobby_id:
                    return request.username in lob["bets"].keys()



class Leave(BaseModel):
    id_game:str
    username:str 
    author:str

app.post("/leave/game")
async def leave_game(request:Leave):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lobby in user["lobbys"]:
                if lobby["id"] == request.id_game:
                    ind = user["lobbys"].index(lobby)
                    user["lobbys"].pop(ind)
                    with open("lobby.json","w") as file:
                        json.dump(data,file)
                    return True
    raise HTTPException(status_code=400,detail="Bad data")

@app.post("/join/game")
async def join_game(request:Leave):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lobby in user["lobbys"]:
                if lobby["id"] == request.id_game:
                    lobby["players"].append(request.username)
                    with open("lobby.json","w") as file:
                        json.dump(data,file)
                    return
    raise HTTPException(status_code=400,detail="Bad data")



def is_lobby_open(author:str,lobby_id:str) -> bool:
    try:
        with open("lobby.json","r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == author:
                for lob in user["lobbys"]:
                    if lob["id"] == lobby_id:
                        return lob["open"] 
    except Exception as e:
        print(f"Exception as {e}")   
                    


@app.get("/join/random/game/{username}")
async def join_random(username:str):
    with open("lobby.json","r") as file:
        data = json.load(file)
    user = random.choice(data)
    open_user_lob = [lob for lob in user["lobbys"] if is_lobby_open(lob)]
    while len(open_user_lob) == 0:
        user = random.choice(data)
        open_user_lob = [lob for lob in user["lobbys"] if is_lobby_open(lob)]
    random_username = user["username"]
    random_game = random.choice(open_user_lob)
    rand_id= random_game["id"]
    for user in data:
        if user["username"] == random_username:
            for lob in user["lobbys"]:
                if lob["id"] == rand_id:
                    lob["players"].append(username)
                    with open("lobby.json","w") as file:
                        json.dump(data,file)
                    return {"Title":lob["title"],"Id":lob["id"],"Host":lob["host"],"Winners":lob["winners"],"Losers":lob["losers"]}

class GetPartyInfo(BaseModel):
    author:str
    id:str
@app.post("/get/party/info")
async def get_party_info(request:GetPartyInfo):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for part in user["lobbys"]:
                if part["id"] == request.id:
                    return {"Host:":part["host"],"Title":part["title"],"Id":part["id"],"Players":part["players"],"Bets":part["bets"]}     
    raise HTTPException(status_code=400,detail="User not found")

class StartNewGame(BaseModel):
    host:str
    id_game:str
@app.post("/start/new_game")
async def start_new_game(request:StartNewGame):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.host:
            for lob in user["lobbys"]:
                if lob["id"] == request.id_game:
                    lob["players"] = request.username
                    lob["bets"] = []
                    lob["winner"] = ""
                    with open("lobby.json","w") as file:
                        json.dump(data,file)
                    return True
    raise HTTPException(status_code=400,detail="Error while updating,try again") 
               

class Win(BaseModel):
    username:str
    author:str
    lobby_id:str
@app.post("/win")
async def win(request:Win,x_system_signature: str = Header(..., alias="X-System-Signature")):
    data_str = json.dumps(request.dict(), sort_keys=True, separators=(',', ':'))
    
    expected_signature = create_signature(data_str, SYSTEM_SECRET)
    
    if not hmac.compare_digest(x_system_signature, expected_signature):
        raise HTTPException(
            status_code=403, 
            detail="Invalid system signature - access denied"
        )
    def is_user(username:str,id_party:str,author:str) -> bool:
        with open("users.json","r") as file:
            data = json.load(file)
        if username in data:
            with open("lobby.json","r") as file:
                lobby = json.load(file)
            for user in lobby:
                if user["username"] == author:
                    for lob in user["lobbys"]:
                        if lob["id"] == id_party:
                            return username in lob["players"]
        return False


    if is_user(request.username):               
                        

        lock = FileLock("lobby.json.lock")
        with lock:
            with open("lobby.json","r") as file:
                data = json.load(file)
            for user in data:
                if user["username"] == request.author:
                    for lob in user["lobbys"]:
                        if lob["id"] == request.lobby_id:
                            lob["winner"] = request.username       
                            with open("lobby.json","w") as file:
                                json.dump(data,file)
                            return True
            raise HTTPException(status_code=400,detail="Error while waiting for the  win")    
    else:
        raise HTTPException(status_code=400,detail="User is not in the system or this user is not in the game")                 


@app.get("get/me/{username}")
async def get_me(username:str):
    try:
        with open("lobby.json","r") as file:
            data = json.load(file)
        result = []
        part = []
        for user in data:
            if user["username"] == username:
                result.append(user["lobbys"])
                break
        for user in data:
            if user["username"] != username:
                for lob in user["lobbys"]:
                    if username in user["lobbys"]:
                        part.append(lob)
        return {"Your lobbies":result,"Lobbies you are in":part}            
    except Exception as e:
        raise HTTPException(status_code=400,detail = f"Error while get_me : {e}")                
                




def delete_all_user_data_from_game(author:str,lobby_id:str,username:str) -> bool:
    with open("lobby.json","r") as file:
        data = json.load(file)
    found = False   
    for user in data:
        if user["username"] == author:
            for lob in user["lobbys"]:
                if lob["id"] == lobby_id:
                    found = True
                    for bet in lob["bets"]:
                        if bet["username"] == username:
                            ind = lob["bets"].index(bet)
                            lob["bets"].pop(ind)
                    if username  == lob["winner"]:
                        lob["winner"] = ""
    if found:
        with open("lobby.json","w") as file:
            json.dump(data,file)
        return True     
    return False                             


class Kick(BaseModel):
    username:str
    author:str
    lobby_id:str                                    

@app.post("/kick")
async def kick(request:Kick):
    with open("lobby.json","r") as file:
        data = json.load(file)
    for user in data:
        if user["username"] == request.author:
            for lob in user["lobbys"]:
                if lob["id"] == request.lobby_id:
                    if lob["host"] == request.author:
                        if request.username in lob["players"]:
                            ind = lob["players"].index(request.username)
                            lob["players"].pop(ind)
                            with open("lobby.json","w") as file:
                                json.dump(data,file)
                            delete_all_user_data_from_game(
                                author=request.username,
                                lobby_id=lob["id"],
                                username=request.username
                            )    
                        else:
                            raise HTTPException(status_code=404,detail="Error user is not in the game")
                    else:
                        raise HTTPException(status_code=403,detail="You are not the host of this game")    

class Commis(BaseModel):
    payment:int # покупка юзера
    commis:int # процент коммиссии

@app.post("/com")
def count_procent(request:Commis) -> Any:
    Ludice_gets = request.payment / request.commis
    user_gets = request.payment - Ludice_gets
    return {"User gets":user_gets,"Ludice gets":user_gets}

class GetUserWin(BaseModel):
    username:str
    author:str
    id_lobby:str
async def get_user_win(request:GetUserWin):
    with open("lobby.json","r") as file:
        data = json.load(file)
    total = 0   
    found = False 
    try:
        for user in data:
            if user["username"] == request.author:
                for lob in user["lobbys"]:
                    if lob["id"]  == request.id:
                        for bet in lob["bets"].values():
                            total += bet
                        found = True
                        break
        if found:
            return total  
        raise HTTPException(status_code=400,detail="Something went wrong")          
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Excpeiotion as {e}")


redis_balance = redis.Redis('localhost',6378,0,decode_responses=True) 
@app.get("/create/{username}/balance")
async def create_user_balance(username:str):
    try:
        if redis_balance.exists(username):
            raise HTTPException(status_code=400,detail="User is alredy in database")
        
        else:
            redis_balance.set(username,0)
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error in redis base: {e}")        

@app.get("/get/{username}/balance")
async def get_user_balance(username:str):
    try:
        if not redis_balance.exists(f"user:{username}"):
            raise HTTPException(status_code=400,detail="User not found")
        else:
            return int(redis_balance.get(username))       
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Exception in redis : {e}")    