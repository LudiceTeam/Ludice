import argparse
import json
import uuid
from fastapi import FastAPI,HTTPException,Header,Depends
from pydantic import Field,BaseModel
import uuid
import time
import hmac


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