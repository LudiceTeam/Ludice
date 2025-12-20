from sqlalchemy import Table,Column,MetaData,String,Integer,Boolean


metadata_obj = MetaData()

drop_table = Table(
    "drop_table",
    metadata_obj,
    Column("id",String,primary_key=True),
    Column("username",String),
    Column("result",Integer),
    Column("bet",Integer),
    Column("won",Boolean)
)