from fastapi import FastAPI,Header,HTTPException
import requests
import uvicorn
import time
from pydantic import BaseModel,Field
import uuid
import json
import hmac
import hashlib

app = FastAPI()




@app.get("/")
async def main():
    return "BackUp"


data_base = {
    "bank":"bank.json",
    "users":"users.json",
    "stats":"stats.json",
    "key":"secrets.json"
}

def get_key() -> str:
    with open(data_base["key"],"r") as file:
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


def wirte_default_bank(username:str) -> bool:
    try:
        with open(data_base["bank"],"r") as file:
            data = json.load(file)
        data.append({
            "username":username,
            "balance":0
        })    
        with open(data_base["bank"],"w") as file:
            json.dump(data,file)
        return True    
    except Exception as e:
        return False

class Increase_Balacne(BaseModel):
    username:str
    amount:str
    signature:str
    timestamp:float = Field(default_factory=time.time)    
@app.post("/incr")
async def inc(request:Increase_Balacne):
    request_dict = request.model_dump()
    if not verify_signature(request_dict,request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")
    try:
        with open(data_base["bank"],"r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == request.username:
                user["balance"] += request.amount
                with open(data_base["bank"],"w") as file:
                    json.dump(data,file)
                return True
        raise HTTPException(status_code=404,detail="User not found")           
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")    


@app.post("/withdraw")
async def witdraw(request:Increase_Balacne):
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")
    try:
        with open(data_base["bank"],"r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == request.username:
                if user["balance"] >= request.amount:
                    user["balance"] -= request.amount
                    with open(data_base["bank"],"w") as file:
                        json.dump(data,file)
                else:
                    raise HTTPException(status_code=400,detail="User doesnt have that much money")            
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")


class AddGaneStat(BaseModel):
    username:str 
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/add")
async def add_game(request:AddGaneStat):
    if verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=400,detail="Invalid siganture")
    try:
        with open(data_base["stats"],"r") as file:
            data = json.load(file)
        for user in data:
            if user["username"] == request.username:
                user["total_games"] += 1
                with open(data_base["stats"],"w") as file:
                    json.dump(data,file)
                return True
        raise HTTPException(status_code=404,detail="Error user not found :(")        
                    
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Smth went wrong : {e}")   
class WriteDefData(BaseModel):
    username:str
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/def/bank")
async def def_bank(request:WriteDefData):
    if not verify_signature(request.model_dump(),request.signature):
        raise HTTPException(status_code=403,detail="Invalid signature")

    try:
        ind  = wirte_default_bank(username=request.username)
        return ind
    except Exception as e:
        raise HTTPException(status_code=400,detail=f"Error : {e}")        