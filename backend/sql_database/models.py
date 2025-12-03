from sqlalchemy import Table,Column,String,Integer,MetaData
from sqlalchemy.dialects.postgresql import JSONB

metadata_obj = MetaData()

table = Table(
    "main_data",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("balance",Integer),
    Column("lobbys",JSONB),
    Column("wins",Integer),
    Column("loses",Integer)
)
