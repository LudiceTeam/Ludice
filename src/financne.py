import requests as req
import json
from pydantic import Field,BaseModel
from fastapi import FastAPI,HTTPException,Header
import time 
import hmac
import hashlib


KEY = ""
def verify_signature(data: dict, received_signature: str) -> bool:
    if time.time() - data.get('timestamp', 0) > 300:
        return False
    
    
    data_to_verify = data.copy()
    data_to_verify.pop("signature", None)
    
    data_str = json.dumps(data_to_verify, sort_keys=True, separators=(',', ':'))
    expected_signature = hmac.new(KEY.encode(), data_str.encode(), hashlib.sha256).hexdigest()
    
    return hmac.compare_digest(received_signature, expected_signature)


app = FastAPI()
@app.get("/")
async def main():
    return "Finance API"

#Payment Interface
class Payment:
    def __init__(self):
        pass
    def pay():
        pass

class TON_Payment(Payment):
    def __init__(self,base_url:str,api_token:str):
        self.base_url = base_url
        self.token = api_token
    def pay(self,from_ton:str,to_user:str,amount:int,message:str = ""):
        payload = {
            "from_wallet": from_ton, 
            "to_username": to_user,      
            "star_amount": amount,     
            "message": message,             
            "currency": "TON"               
        }
        
        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {self.token}" if self.token else ""
        }
        response = req.post(
            f"{self.base_url}/sendStars", 
            json=payload, 
            headers=headers
        )
        return response.json()
def get_token():
    pass

def get_url():
    pass

class Pay(BaseModel):
    username:str
    amount:int
    message:str
    signature:str
    timestamp:float = Field(default_factory=time.time)
@app.post("/user/pay")
async def pay(request:Pay):
    pass







