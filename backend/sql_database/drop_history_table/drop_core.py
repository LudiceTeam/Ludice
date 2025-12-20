from drop_models import metadata_obj,drop_table
from drop_sqli import sync_engine
from sqlalchemy import select,update,insert,delete


def create_table():
    metadata_obj.create_all(sync_engine)
create_table()    