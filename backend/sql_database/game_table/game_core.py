from sqlalchemy import text,select,and_
from game_sql import sync_engine
from game_models import metadata_obj,game_table
import uuid
from typing import List,Optional



def create_table():
    #metadata_obj.drop_all(sync_engine)
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


def start_game_database(username:str,bet:int) -> str:
    with sync_engine.connect() as conn:
        try:
            stmt = select(game_table).where(
                and_(
                    text("array_length(players, 1) = 1"),
                    game_table.c.bet == bet
                )
            )
            res = conn.execute(stmt)
            data = res.fetchall()
            found = False
            if data is not  None:
                for game in data:
                    if username not in game[1]:
                        found = True
                        game[1].append(username)
                        update_stmt = game_table.update().where(game_table.c.id == game[2]).values(players = game[1])
                        conn.execute(update_stmt)
                        conn.commit()
                        return game[2]
            if not found:
                try:
                    print("test")
                    stmt_2 = select(game_table.c).where(
                        and_(
                            #text("players IS NULL OR array_length(players, 1) = 0"),
                            game_table.c.bet == 0
                        )
                    )      
                    res = conn.execute(stmt_2)
                    data = res.fetchone()
                    if data is not None:
                        update_stmt = game_table.update().where(game_table.c.id == data[2]).values(bet = bet,players = [username])
                        conn.execute(update_stmt)
                        conn.commit()
                    else:
                        print("Nothing found")    
                except Exception as e:
                    raise Exception(f"Error : {e}")    
        except Exception as e:
            raise Exception(f"Error : {e}")
def cancel_game(username:str,id:str):
    with sync_engine.connect() as conn:
        try:
            pass
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
print(start_game_database("user1",10))