from sqlalchemy import text,select
from history_sqli import sync_engine
from history_models import metadata_obj,history_table
import uuid



def create_table():
    metadata_obj.create_all(sync_engine)
    