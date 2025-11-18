import argparse
import json
import uuid
from fastapi import FastAPI,HTTPException,Header,Depends,Request
from pydantic import Field,BaseModel
import uuid
import time
import hmac
import hashlib



def get_special_key() -> str:
    try:
        with open("secrets.json","r") as file:
            data  = json.load(file)
        return data["key"]    
    except Exception as e:
        print(f"Error : {e}")
        raise KeyError("Error")

def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    KEY = get_special_key()
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)


path = "/Users/vikrorkhanin/Ludice/data/game.json"
parser = argparse.ArgumentParser(description='Generate empty json lobby')
parser.add_argument('-c', '--count', type=int, help='Amount of empty lobbies')
def write_empty():
    try:
        with open(path,"r") as file:
            data = json.load(file)
        data.append({
            "id":str(uuid.uuid4()),
            "players":[],
            "bet":0,
            "winner":""
        })
        with open(path,"w") as file:
            json.dump(data,file)
    except Exception as e:
        raise TypeError(f"Error : {e}")
args = parser.parse_args()
if args.count:
    for i in range(args.count):
        write_empty()
else:
    print("Wrong arguments")    

def get_api_key() -> str:
    try:
        with open("secrets.json","r") as file:
            data  = json.load(file)
        return data["api"]    
    except Exception as e:
        print(f"Error : {e}")
        raise KeyError("Error")

async def safe_get(req:Request):
    api = req.headers.get("X-API-KEY")
    if not api or not hmac.compare_digest(api,get_api_key()):
        raise HTTPException(status_code=403,detail = "Forbitten")

app = FastAPI()

@app.get("/")
async def main():
    return "API for empty lobby"

