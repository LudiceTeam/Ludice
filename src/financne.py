import requests as req
import json
from pydantic import Field,BaseModel
from fastapi import FastAPI,HTTPException,Header


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






