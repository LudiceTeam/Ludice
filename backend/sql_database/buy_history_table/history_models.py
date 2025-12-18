from sqlalchemy import Table,String,Integer,MetaData,Column,ARRAY
from sqlalchemy.dialects.postgresql import JSONB


metadata_obj = MetaData()

history_table = Table(
    "history_data",
    metadata_obj,
    Column("username",String,primary_key=True),
    Column("name",String),
    Column("id",String),
    Column("price",Integer)
)