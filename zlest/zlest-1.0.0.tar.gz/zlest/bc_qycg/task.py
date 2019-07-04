import time

from zlest.bc_qycg import bc_www_bidding_citic


from lmf.dbv2 import db_command

from zlest.util.conf import get_conp,get_conp1

#1
def task_bc_www_bidding_citic(**args):
    conp=get_conp(bc_www_bidding_citic._name_)
    bc_www_bidding_citic.work(conp,pageloadtimeout=180,**args)



def task_all():
    bg=time.time()
    try:
        task_bc_www_bidding_citic()
    except:
        print("part1 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zlest')
    arr=["www_bidding_citic",]
    for diqu in arr:
        sql="create schema if not exists %s"% ('bc__'+diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




