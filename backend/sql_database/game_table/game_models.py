from sqlalchemy import Table,String,Integer,MetaData,Column,ARRAY
from sqlalchemy.dialects.postgresql import JSONB


metadata_obj = MetaData()

game_table = Table(
    "game_data",
    metadata_obj,
    Column("bet",Integer),
    Column("players",ARRAY(String)),
    Column("id",String,primary_key=True),
    Column("winner",String),
    Column("results",JSONB)
)