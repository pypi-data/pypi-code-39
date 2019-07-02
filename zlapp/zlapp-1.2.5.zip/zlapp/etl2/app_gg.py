import time 
from lmf.dbv2 import db_command,db_query
import traceback
from lmf.bigdata import pg2pg 
from sqlalchemy.dialects.postgresql import  TEXT,BIGINT,TIMESTAMP,NUMERIC


def gg_all():
    sql="select * from etl.gg_all  "
    conp_hawq=["gpadmin","since2015","192.168.4.179","base_db","v3"]
    conp_pg=["postgres","since2015","192.168.4.188","bid","public"]
    datadict={"html_key":BIGINT(),
    "price":NUMERIC(),'bd_key':BIGINT(),'fa_butime':TIMESTAMP(0),'create_time':TIMESTAMP(0)}
    pg2pg(sql,'gg',conp_hawq,conp_pg,chunksize=10000,datadict=datadict)


def gg_all_pk():
    conp_pg=["postgres","since2015","192.168.4.188","bid","public"]
    sql="alter table public.gg add constraint pk_gg_html_key primary key(html_key) "
    db_command(sql,dbtype="postgresql",conp=conp_pg)



def gg_cdc():
    sql="select * from etl.gg_cdc  "
    conp_hawq=["gpadmin","since2015","192.168.4.179","base_db","v3"]
    conp_pg=["postgres","since2015","192.168.4.188","bid","cdc"]
    datadict={"html_key":BIGINT(),
    "price":NUMERIC(),'bd_key':BIGINT(),'fa_butime':TIMESTAMP(0),'create_time':TIMESTAMP(0)}
    pg2pg(sql,'gg_cdc',conp_hawq,conp_pg,chunksize=10000,datadict=datadict)

    sql="insert into public.gg select * from cdc.gg_cdc"
    db_command(sql,dbtype="postgresql",conp=conp_pg)




def est():
    conp_pg=["postgres","since2015","192.168.4.188","bid","public"]

    sql="select tablename from pg_tables where schemaname='public' "

    df=db_query(sql,dbtype='postgresql',conp=conp)

    if 'gg' not in df['tablename']:
        print("gg表不存在，需要全量导入")
        gg_all()
        gg_all_pk()
    else:
        print("gg表已经存在，增量更新")
    gg_all()
    gg_all_pk()

