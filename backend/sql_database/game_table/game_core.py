from sqlalchemy import text,select
from game_sql import sync_engine
from game_models import metadata_obj,game_table
import uuid
from typing import List,Optional
from sqlalchemy import func



def create_table():
    metadata_obj.create_all(sync_engine)


def fill_empty():
    with sync_engine.connect() as conn:
        try:
            stmt = game_table.insert().values(
                bet = 0,
                players = [],
                id = str(uuid.uuid4()),
                winner = ""
            )
            conn.execute(stmt)
            conn.commit()
        except Exception as e:
            raise Exception(f"Error : {e}")


def start_game_database(username:str,bet:int):
    with sync_engine.connect() as conn:
        try:
            stmt = select(game_table.c.id).where(func.array_length(game_table.c.players,1) == 1)
            res = conn.execute(stmt)
            data = res.fetchone()
            if  data is None:
                print(data)
        except Exception as e:
            raise Exception(f"Error : {e}")
def get_all_data():
    with sync_engine.connect() as conn:
        try:
            stmt = select(game_table)
            res = conn.execute(stmt)
            return res.fetchall()
        except Exception as e:
            raise Exception(f"Error : {e}")
print(get_all_data())
        