from sqlalchemy import text,select
from sql_database.sql_i import sync_engine
from sql_database.models import metadata_obj,table
import uuid
from typing import List,Optional


def create_table():
    metadata_obj.create_all(sync_engine)


def is_users_exists(username:str) -> bool:
    with sync_engine.connect() as conn:
        stmt = select(text("COUNT(1)")).where(table.c.username == username)
        conn.execute(stmt)
        res = conn.scalar()
        return res > 0 if res else False

def register(username:str) -> bool:
    if is_users_exists(username):
        raise KeyError("User already exists")
    with sync_engine.connect() as conn:
        try:
            stmt = table.insert().values(
                username = username,
                balance = 0,
                lobbies = [],
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
        
        
