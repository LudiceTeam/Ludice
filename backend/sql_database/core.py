from sqlalchemy import text,select
from sql_database.sql_i import sync_engine
from sql_database.models import metadata_obj,table
import uuid
from typing import List,Optional


def create_table():
    metadata_obj.create_all(sync_engine)
    