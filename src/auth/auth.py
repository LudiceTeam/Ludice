import jwt
from datetime import timedelta,datetime



SECRET_KEY = "our_secret_key"
ALGORITHM = "SHA256"

def create_host_data():
    payload = {
        "role":"host",
        "exp": datetime.utcnow() + timedelta(hours=24)
    }
    token = jwt.encode(payload, SECRET_KEY, algorithm=ALGORITHM)
    return token

def crete_system_token():
    payload = {
        "role":"Ludice",
        "exp":datetime.utcnow() + timedelta(hours = 24)
    }
    token = jwt.encode(payload,SECRET_KEY, algorithm = ALGORITHM)
    return token



def check_is_user_system(token:str) -> bool:
    try:
        payload = jwt.decode(token,SECRET_KEY,ALGORITHM)
        return payload.get("role") == "Ludice"
    except jwt.JWTERROR:
        return False
    