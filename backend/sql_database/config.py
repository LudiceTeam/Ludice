from dotenv import load_dotenv
import os


load_dotenv()

def conect():
    #postgresql://[user[:password]@]host[:port]/database[?parameters]
    
    return f"postgresql+psycopg://{os.getenv("DB_USER")}:{os.getenv("DB_PASSWORD")}@localhost:5432/ai_data" 
