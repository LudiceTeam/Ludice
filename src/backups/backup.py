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
    except Exception as e:
        return False
    



