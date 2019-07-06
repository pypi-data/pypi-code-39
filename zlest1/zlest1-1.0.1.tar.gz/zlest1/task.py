import time

from zlest1 import bidding_sinopec_com
from zlest1 import eps_shmetro_com
from zlest1 import mall_cdtbuy_cn

from zlest1 import www_bidding_citic
from zlest1 import www_haierbid_com
from zlest1 import www_hnbidding_com
from zlest1 import www_hnzbcg_com_cn

from zlest1 import qg_ggzy
from zlest1 import qg_zfcg

from lmf.dbv2 import db_command

from zlest1.util.conf import get_conp,get_conp1

#1
def task_www_bidding_citic(**args):
    conp=get_conp(www_bidding_citic._name_)
    www_bidding_citic.work(conp,pageloadtimeout=180,**args)


#2
def task_bidding_sinopec_com(**args):
    conp=get_conp(bidding_sinopec_com._name_)
    bidding_sinopec_com.work(conp,pageloadtimeout=180,**args)

#3
def task_eps_shmetro_com(**args):
    conp=get_conp(eps_shmetro_com._name_)
    eps_shmetro_com.work(conp,pageloadtimeout=180,**args)


#4
def task_mall_cdtbuy_cn(**args):
    conp=get_conp(mall_cdtbuy_cn._name_)
    mall_cdtbuy_cn.work(conp,pageloadtimeout=180,**args)


#5
def task_www_haierbid_com(**args):
    conp=get_conp(www_haierbid_com._name_)
    www_haierbid_com.work(conp,pageloadtimeout=180,**args)


#6
def task_www_hnbidding_com(**args):
    conp=get_conp(www_hnbidding_com._name_)
    www_hnbidding_com.work(conp,pageloadtimeout=180,**args)


#7
def task_www_hnzbcg_com_cn(**args):
    conp=get_conp(www_hnzbcg_com_cn._name_)
    www_hnzbcg_com_cn.work(conp,pageloadtimeout=180,**args)

#8
def task_qg_ggzy(**args):
    conp = get_conp(qg_ggzy._name_)
    qg_ggzy.work(conp, pageloadtimeout=180, **args)


#9
def task_qg_zfcg(**args):
    conp = get_conp(qg_zfcg._name_)
    qg_zfcg.work(conp, pageloadtimeout=180, **args)


def task_all():
    bg=time.time()
    try:
        task_www_bidding_citic()
        task_bidding_sinopec_com()
        task_eps_shmetro_com()
        task_mall_cdtbuy_cn()
        task_www_haierbid_com()

    except:
        print("part1 error!")

    try:
        task_www_hnbidding_com()
        task_www_hnzbcg_com_cn()
        task_qg_ggzy()
        task_qg_zfcg()
    except:
        print("part2 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zlest1')
    arr=["www_bidding_citic","bidding_sinopec_com","eps_shmetro_com","qg_zfcg","qg_ggzy",

         "mall_cdtbuy_cn","www_haierbid_com","www_hnbidding_com","www_hnzbcg_com_cn"]
    for diqu in arr:
        sql="create schema if not exists %s"% (diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




