from drop_models import metadata_obj,drop_table
from drop_sqli import sync_engine
from sqlalchemy import select,update,delete
import uuid

def create_table():
    metadata_obj.create_all(sync_engine)


def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(drop_table)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise Exception(f"Error : {e}") 
def write_user_drop(username:str,result:int,bet:int,won:bool):
    with sync_engine.connect() as conn:
        try:
            stmt = drop_table.insert().values(
                id = str(uuid.uuid4()),
                username = username,
                result = result,
                bet = bet,
                won = won
            )
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            return Exception(f"Error  : {e}")
def get_user_history(username:str):
    with sync_engine.connect() as conn:
        try:
            stmt = select(drop_table ).where(drop_table.c.username == username)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            return Exception(f"Error : {e}")   
def clear_user_history(username:str):
    with sync_engine.connect() as conn:
        try:
            stmt = delete(drop_table).where(drop_table.c.username == username)
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            return Exception(f"Error : {e}")       