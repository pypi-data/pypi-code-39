import time

from zlest.bc_qycg import bc_bidding_sinopec_com
from zlest.bc_qycg import bc_eps_shmetro_com
from zlest.bc_qycg import bc_mall_cdtbuy_cn

from zlest.bc_qycg import bc_www_bidding_citic
from zlest.bc_qycg import bc_www_haierbid_com
from zlest.bc_qycg import bc_www_hnbidding_com
from zlest.bc_qycg import bc_www_hnzbcg_com_cn

from lmf.dbv2 import db_command

from zlest.util.conf import get_conp,get_conp1

#1
def task_bc_www_bidding_citic(**args):
    conp=get_conp(bc_www_bidding_citic._name_)
    bc_www_bidding_citic.work(conp,pageloadtimeout=180,**args)


#2
def task_bc_bidding_sinopec_com(**args):
    conp=get_conp(bc_bidding_sinopec_com._name_)
    bc_bidding_sinopec_com.work(conp,pageloadtimeout=180,**args)

#3
def task_bc_eps_shmetro_com(**args):
    conp=get_conp(bc_eps_shmetro_com._name_)
    bc_eps_shmetro_com.work(conp,pageloadtimeout=180,**args)


#4
def task_bc_mall_cdtbuy_cn(**args):
    conp=get_conp(bc_mall_cdtbuy_cn._name_)
    bc_mall_cdtbuy_cn.work(conp,pageloadtimeout=180,**args)


#5
def task_bc_www_haierbid_com(**args):
    conp=get_conp(bc_www_haierbid_com._name_)
    bc_www_haierbid_com.work(conp,pageloadtimeout=180,**args)


#6
def task_bc_www_hnbidding_com(**args):
    conp=get_conp(bc_www_hnbidding_com._name_)
    bc_www_hnbidding_com.work(conp,pageloadtimeout=180,**args)


#7
def task_bc_www_hnzbcg_com_cn(**args):
    conp=get_conp(bc_www_hnzbcg_com_cn._name_)
    bc_www_hnzbcg_com_cn.work(conp,pageloadtimeout=180,**args)



def task_all():
    bg=time.time()
    try:
        task_bc_www_bidding_citic()
        task_bc_bidding_sinopec_com()
        task_bc_eps_shmetro_com()
        task_bc_mall_cdtbuy_cn()
        task_bc_www_haierbid_com()
        task_bc_www_hnbidding_com()
        task_bc_www_hnzbcg_com_cn()
    except:
        print("part1 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zlest')
    arr=["www_bidding_citic","bidding_sinopec_com","eps_shmetro_com",

         "mall_cdtbuy_cn","www_haierbid_com","www_hnbidding_com","www_hnzbcg_com_cn"]
    for diqu in arr:
        sql="create schema if not exists %s"% (diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




