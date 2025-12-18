from sqlalchemy import text,select,delete
from history_sqli import sync_engine
from history_models import metadata_obj,history_table
import uuid
from typing import List
from datetime import datetime



def create_table():
    #metadata_obj.drop_all(sync_engine)
    metadata_obj.create_all(sync_engine)
def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(history_table)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            return Exception(f"Error  {e}")
def create_new_buy(username:str,name:str,price:str):
    with sync_engine.connect() as conn:
        try:
            stmt = history_table.insert().values(
                username = username,
                name = name,
                id = str(uuid.uuid4()),
                price = price,
                date = str(datetime.now()).split()[0]
            )
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            return Exception(f"Error : {e}")   
def get_user_history(username:str) -> List:
    with sync_engine.connect() as conn:
        try:
            stmt = select(history_table).where(history_table.c.username == username)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            return Exception(f"Error : {e}")
                