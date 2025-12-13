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
                wins = 0,
                loses = 0,
                games_count = 0,
                sogl = False,
                down_payment = True
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
def count_procent_of_wins(username:str) -> float:
    def get_user_wins() -> int:
        with sync_engine.connect() as conn:
            try:
                stmt = select(table.c.wins).where(table.c.username == username)
                res = conn.execute(stmt)
                data = res.fetchall()
                if data is not None:
                    return int(data[0][0])
                return None
            except Exception as e:
                return Exception(f"Error : {e}")        
    def get_user_games_count() -> int:
        with sync_engine.connect() as conn:
            try:
                stmt = select(table.c.games_count).where(table.c.username == username)
                res = conn.execute(stmt)
                data = res.fetchall()
                if data is not None:
                    return int(data[0][0])
                return None
            except Exception as e:
                return Exception(f"Error : {e}")    
    wins = get_user_wins()
    games_count = get_user_games_count()
    if (type(wins) != int or type(games_count) != int) or (games_count == 0 or wins ==  0):
        return 0        
    else:
        return (games_count // wins) * 100
def get_leader_borad_games() -> dict:
    with sync_engine.connect() as conn:
        try:
            stmt = select(table.c.username)
            res = conn.execute(stmt)
            data = res.fetchall()
            users = []
            for user in data:
                users.append(user[0])
            stmt_games = select(table.c.games_count)
            res_games = conn.execute(stmt_games)
            data2 = res_games.fetchall()
            counts = []
            for count in data2:
                counts.append(count[0])
            data_leader_board = {}
            for i in range(len(users)):
                data_leader_board[users] = counts[i]
            return data_leader_board    
        except Exception as e:
            return Exception(f"Error : {e}")    
def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(table)
            res = conn.execute(stmt)
            data = res.fetchall()
            print(data)
        except Exception as e:
            return Exception(f"Error : {e}")  
def get_me(username:str) -> dict:
    if not is_users_exists(username):
        return KeyError("User not found")
    with sync_engine.connect() as conn:
        def get_wins():
            stmt = select(table.c.wins).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchall()
            if data is not None:
                return data[0][0]
        def get_loses():
            stmt = select(table.c.loses).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchall()
            if data is not None:
                return data[0][0]
        def get_games_count():
            stmt = select(table.c.games_count).where(table.c.username == username)
            res = conn.execute(stmt)
            data = res.fetchall()
            if data is not None:
                return data[0][0]   
        try:
            balance  = get_user_balance(username)
            wins = get_wins()
            loses = get_loses()
            total_games = get_games_count()
            win_procent = count_procent_of_wins(username)
            #print(win_procent)
            result = {
                "Tatal games":total_games,
                "Wins":wins,
                "Loses":loses,
                "Balance":balance,
                "Wins procent":win_procent
            }
            return result
        except Exception as e:
            return Exception(f"Error : {e}")