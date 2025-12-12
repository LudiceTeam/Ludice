from sqlalchemy import text,select,and_,func
from sql_i import sync_engine
from models import metadata_obj,table
import uuid
from typing import List,Optional
import os
from dotenv import load_dotenv
from typing import List,Optional


def create_table():
    metadata_obj.create_all(sync_engine)

def check_user_dowm_payment(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.down_payment).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()
            if data is not None:
                return bool(data)
        except Exception as e:
            raise Exception(f"Error : {e}")



def is_users_exists(username:str) -> bool:
    with sync_engine.connect() as conn:
        stmt = select(table.c.username).where(table.c.username == username)
        res = conn.execute(stmt)
        data = res.fetchone()
        if data is not None:
            return len(data[0]) > 0
        return False 

def register(username:str) -> bool:
    if is_users_exists(username):
        raise KeyError("User already exists")
    with sync_engine.connect() as conn:
        try:
            stmt = table.insert().values(
                username = username,
                balance = 100,
                games = [],
                wins = 0,
                loses = 0
            )
            conn.execute(stmt)
            conn.commit()
            return True
        except Exception as e:
            raise Exception(f"Error : {e}")
def write_soglasion(username:str,res:True):
    if not is_users_exists(username):
        raise KeyError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.sogl).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()
            update_stmt = table.update().where(table.c.username == username).values(sogl = res)
            conn.execute(update_stmt)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error : {e}")  
def check_sogl(username:str) -> bool:
    if not is_users_exists(username):
        raise KeyError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.sogl).where(table.c.username == username)
            return conn.execute(stmt).fetchone()[0]
        except Exception as e:
            raise Exception(f"Error : {e}")  


def decrease_user_balance(username:str,amount:int) -> bool:
    if not is_users_exists(username):
        raise KeyError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.balance).where(table.c.username == username)
            res = conn.execute(stmt)
            user_balance = res.fetchone()[0]
            if user_balance < amount:
                return False
            update_stmt = table.update().where(table.c.username == username).values(balance = user_balance - amount)
            conn.execute(update_stmt)
            conn.commit()
            return True
        except Exception as e:
            raise Exception(f"Error : {e}")
def increase_user_balance(username:str,amount:int) -> bool:
    if not is_users_exists(username):
        raise KeyError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.balance).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()[0]
            if data:
                update_stmt = table.update().where(table.c.username == username).values(balance = data + amount)
                conn.execute(update_stmt)
                conn.commit()
                return True
            return False
        except Exception as e:
            raise Exception(f"Error : {e}")   
def get_user_balance(username:str) -> int:
    if not is_users_exists(username):
        raise KeyError("User not found")
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.balance).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchone()[0]
            return int(data)
        except Exception as e:
            raise Exception(f"Error : {e}")   
def count_all_user_money() -> int:
    with sync_engine.connect()  as conn:
        try:
            stmt = select(table)
            res = conn.execute(stmt)
            data = res.fetchall()
            result:int = 0
            for user_ in data:
                result += int(user_[1]) # Тут кортеж и баланс это втроая Column(см. models.py)
            return result    
        except Exception as e:
            raise Exception(f"Error : {e}")  
def plus_one_win(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.wins).where(table.c.username == username)
            res = conn.execute()
            data = res.fetchone()[0]
            if data is not None:
                update_stmt = table.update().where(table.c.username == username).values(wins = data + 1)
                conn.execute(update_stmt)
                conn.commit()
                return True 
            else:
                print("User not found")
                return False
        except Exception as e:
            print(f"Error : {e}") 
            raise Exception(f"Error : {e}")       

def plus_one_game(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.games_count).where(table.c.username == username)
            res = conn.execute()
            data = res.fetchone()[0]
            if data is not None:
                update_stmt = table.update().where(table.c.username == username).values(games_count = data + 1)
                conn.execute(update_stmt)
                conn.commit()
                return True 
            else:
                print("User not found")
                return False
        except Exception as e:
            print(f"Error : {e}") 
            raise Exception(f"Error : {e}")       

def plus_one_lose(username:str) -> bool:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.loses).where(table.c.username == username)
            res = conn.execute()
            data = res.fetchone()[0]
            if data is not None:
                update_stmt = table.update().where(table.c.username == username).values(loses = data + 1)
                conn.execute(update_stmt)
                conn.commit()
                return True 
            else:
                print("User not found")
                return False
        except Exception as e:
            print(f"Error : {e}") 
            raise Exception(f"Error : {e}")       
def count_procent_of_wins(username) -> float:
    def get_user_wins() -> int:
        with sync_engine.connect() as conn:
            try:
                stmt = select(table.c.wins).where(table.c.username == username)
                res = conn.execute(stmt)
                data = res.fetchone()[0]
                if data is not None:
                    return int(data)
                return None
            except Exception as e:
                return Exception(f"Error : {e}")        
    def get_user_games_count() -> int:
        with sync_engine.connect() as conn:
            try:
                stmt = select(table.c.games_count).where(table.c.username == username)
                res = conn.execute(stmt)
                data = res.fetchone()[0]
                if data is not None:
                    return int(data)
                return None
            except Exception as e:
                return Exception(f"Error : {e}")    
    wins = get_user_wins()
    games_count = get_user_games_count()
    if type(wins) != int or type(games_count) != int:
        raise UserWarning("User not found")        
    else:
        return (games_count // wins) * 100
def get_leader_borad():
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.username)
            res = conn.execute(stmt)
            data = res.fetchall()
            print(data)
        except Exception as e:
            return Exception(f"Error : {e}")    
def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(table)
            res = conn.execute(stmt)
            data = res.fetchall()
            return data
        except Exception as e:
            return Exception(f"Error : {e}")  
print(register("user1"))              