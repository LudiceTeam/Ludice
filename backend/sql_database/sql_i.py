from sqlalchemy import text,create_engine
from config import conect

sync_engine =  create_engine(
    url = conect(),
    echo = False,
    pool_size = 5,
    max_overflow=10,
)
