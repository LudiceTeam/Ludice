from sqlalchemy import Table,Column,String,Integer,Boolean,MetaData
from sqlalchemy.dialects.postgresql import JSONB

metadata_obj = MetaData()

table = Table(
    "main_data",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("balance",Integer),
    Column("wins",Integer),
    Column("loses",Integer),
    Column("games_count",Integer),
    Column("sogl",Boolean),
    Column("down_payment",Boolean)
)
