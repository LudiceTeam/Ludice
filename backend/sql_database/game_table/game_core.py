from sqlalchemy import text,select
from game_sql import sync_engine
from game_models import metadata_obj,game_table
import uuid
from typing import List,Optional



def create_table():
    metadata_obj.create_all(sync_engine)
create_table()