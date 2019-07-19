import time

from zhulong2.guangdong import dongguan
from zhulong2.guangdong import guangzhou
from zhulong2.guangdong import shenghui
from zhulong2.guangdong import shenzhen
# 新增
from zhulong2.guangdong import shantou
from zhulong2.guangdong import zhongshan

# 从省级拆开的省份
from zhulong2.guangdong import chaozhou
from zhulong2.guangdong import dongguan1
from zhulong2.guangdong import foshan
from zhulong2.guangdong import guangzhou1
from zhulong2.guangdong import heyuan
from zhulong2.guangdong import huizhou
from zhulong2.guangdong import jiangmen
from zhulong2.guangdong import jieyang
from zhulong2.guangdong import maoming
from zhulong2.guangdong import meizhou
from zhulong2.guangdong import qingyuan
from zhulong2.guangdong import shantou1
from zhulong2.guangdong import shanwei
from zhulong2.guangdong import shaoguan
from zhulong2.guangdong import shenzhen1
from zhulong2.guangdong import yangjiang
from zhulong2.guangdong import yunfu
from zhulong2.guangdong import zhanjiang
from zhulong2.guangdong import zhaoqing
from zhulong2.guangdong import zhongshan1
from zhulong2.guangdong import zhuhai



from lmf.dbv2 import db_command

from zhulong2.util.conf import get_conp,get_conp1

#1
def task_dongguan(**args):
    conp=get_conp(dongguan._name_)
    dongguan.work(conp,pageloadtimeout=180,**args)

#2
def task_shenghui(**args):
    conp=get_conp(shenghui._name_)
    shenghui.work(conp,pageloadtimeout=180,interval_page=100,**args)

#3
def task_guangzhou(**args):
    conp=get_conp(guangzhou._name_)
    guangzhou.work(conp,pageloadtimeout=180,**args)

#4
def task_shenzhen(**args):
    conp=get_conp(shenzhen._name_)
    shenzhen.work(conp,pageloadtimeout=180,**args)

#5
def task_shantou(**args):
    conp=get_conp(shantou._name_)
    shantou.work(conp,pageloadtimeout=180,**args)

#6
def task_zhongshan(**args):
    conp=get_conp(zhongshan._name_)
    zhongshan.work(conp,pageloadtimeout=180,**args)




def task_chaozhou(**args):
    conp = get_conp(chaozhou._name_)
    chaozhou.work(conp, pageloadtimeout=180, **args)

def task_dongguan1(**args):
    conp = get_conp(dongguan1._name_)
    dongguan1.work(conp, pageloadtimeout=180, **args)

def task_foshan(**args):
    conp = get_conp(foshan._name_)
    foshan.work(conp, pageloadtimeout=180, **args)

def task_guangzhou1(**args):
    conp = get_conp(guangzhou1._name_)
    guangzhou1.work(conp, pageloadtimeout=180, **args)

def task_heyuan(**args):
    conp = get_conp(heyuan._name_)
    heyuan.work(conp, pageloadtimeout=180, **args)

def task_huizhou(**args):
    conp = get_conp(huizhou._name_)
    huizhou.work(conp, pageloadtimeout=180, **args)

def task_jiangmen(**args):
    conp = get_conp(jiangmen._name_)
    jiangmen.work(conp, pageloadtimeout=180, **args)

def task_jieyang(**args):
    conp = get_conp(jieyang._name_)
    jieyang.work(conp, pageloadtimeout=180, **args)

def task_maoming(**args):
    conp = get_conp(maoming._name_)
    maoming.work(conp, pageloadtimeout=180, **args)

def task_meizhou(**args):
    conp = get_conp(meizhou._name_)
    meizhou.work(conp, pageloadtimeout=180, **args)

def task_qingyuan(**args):
    conp = get_conp(qingyuan._name_)
    qingyuan.work(conp, pageloadtimeout=180, **args)

def task_shantou1(**args):
    conp = get_conp(shantou1._name_)
    shantou1.work(conp, pageloadtimeout=180, **args)

def task_shanwei(**args):
    conp = get_conp(shanwei._name_)
    shanwei.work(conp, pageloadtimeout=180, **args)

def task_shaoguan(**args):
    conp = get_conp(shaoguan._name_)
    shaoguan.work(conp, pageloadtimeout=180, **args)

def task_shenzhen1(**args):
    conp = get_conp(shenzhen1._name_)
    shenzhen1.work(conp, pageloadtimeout=180, **args)

def task_yangjiang(**args):
    conp = get_conp(yangjiang._name_)
    yangjiang.work(conp, pageloadtimeout=180, **args)

def task_yunfu(**args):
    conp = get_conp(yunfu._name_)
    yunfu.work(conp, pageloadtimeout=180, **args)

def task_zhanjiang(**args):
    conp = get_conp(zhanjiang._name_)
    zhanjiang.work(conp, pageloadtimeout=180, **args)

def task_zhaoqing(**args):
    conp = get_conp(zhaoqing._name_)
    zhaoqing.work(conp, pageloadtimeout=180, **args)

def task_zhongshan1(**args):
    conp = get_conp(zhongshan1._name_)
    zhongshan1.work(conp, pageloadtimeout=180, **args)

def task_zhuhai(**args):
    conp = get_conp(zhuhai._name_)
    zhuhai.work(conp, pageloadtimeout=180, **args)



def task_all():
    bg=time.time()
    try:
        task_dongguan()
        task_guangzhou()
        task_shenghui()
        task_shenzhen()
        task_shantou()
        task_zhongshan()
    except:
        print("part1 error!")

    try:
        task_chaozhou()
        task_dongguan1()
        task_foshan()
        task_guangzhou1()
        task_heyuan()
    except:
        print("part2 error!")

    try:
        task_huizhou()
        task_jiangmen()
        task_jieyang()
        task_maoming()
        task_meizhou()
    except:
        print("part3 error!")

    try:
        task_qingyuan()
        task_shantou1()
        task_shanwei()
        task_shaoguan()
        task_shenzhen1()
    except:
        print("part4 error!")

    try:
        task_yangjiang()
        task_yunfu()
        task_zhanjiang()
        task_zhaoqing()
        task_zhongshan1()
        task_zhuhai()
    except:
        print("part5 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)




def create_schemas():
    conp=get_conp1('zfcg')
    arr=["guangdong_shenghui","guangdong_dongguan","guangdong_guangzhou",
         "guangdong_shenzhen","guangdong_shantou","guangdong_zhongshan",
         "chaozhou", "dongguan1", "foshan", "guangzhou1", "heyuan", "huizhou", "jiangmen", "jieyang", "maoming",
         "meizhou", "qingyuan", "shantou1", "shanwei", "shaoguan", "shenzhen1", "yangjiang", "yunfu",
         "zhanjiang", "zhaoqing", "zhongshan1", "zhuhai",
         ]
    for diqu in arr:
        sql="create schema if not exists %s"%diqu
        db_command(sql,dbtype="postgresql",conp=conp)


