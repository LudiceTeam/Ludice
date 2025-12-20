from sqlalchemy import create_engine
from drop_config import conect

sync_engine =  create_engine(
    url = conect(),
    echo = False,
    pool_size = 5,
    max_overflow=10,
)