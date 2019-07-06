import time

from zlest import ezhoushi
from zlest import guizhousheng
from zlest import qinghaisheng
from zlest import shaoyangxian
from zlest import shenzhenshi

from zlest import anhuisheng
from zlest import guangdongsheng
from zlest import guangxisheng
from zlest import henansheng
from zlest import hunansheng

from zlest import jiangxisheng

from zlest import wuxishi
from zlest import zhejiangsheng
from zlest import anhuisheng1

from zlest import enshizhou

from zlest import hubeisheng
from zlest import sichuansheng
from zlest import qinghaisheng1
from zlest import neimenggu



from lmf.dbv2 import db_command

from zlest.util.conf import get_conp,get_conp1

#1
def task_ezhoushi(**args):
    conp=get_conp(ezhoushi._name_)
    ezhoushi.work(conp,pageloadtimeout=180,**args)

#2
def task_guizhousheng(**args):
    conp=get_conp(guizhousheng._name_)
    guizhousheng.work(conp,pageloadtimeout=180,**args)

#3
def task_qinghaisheng(**args):
    conp=get_conp(qinghaisheng._name_)
    qinghaisheng.work(conp,pageloadtimeout=180,**args)

#4
def task_shaoyangxian(**args):
    conp=get_conp(shaoyangxian._name_)
    shaoyangxian.work(conp,pageloadtimeout=180,**args)

#5
def task_shenzhenshi(**args):
    conp=get_conp(shenzhenshi._name_)
    shenzhenshi.work(conp,pageloadtimeout=180,**args)
#6
def task_anhuisheng(**args):
    conp=get_conp(anhuisheng._name_)
    anhuisheng.work(conp,pageloadtimeout=180,**args)
#7
def task_guangdongsheng(**args):
    conp=get_conp(guangdongsheng._name_)
    guangdongsheng.work(conp,pageloadtimeout=180,**args)
#8
def task_guangxisheng(**args):
    conp=get_conp(guangxisheng._name_)
    guangxisheng.work(conp,pageloadtimeout=180,**args)
#9
def task_henansheng(**args):
    conp=get_conp(henansheng._name_)
    henansheng.work(conp,pageloadtimeout=180,**args)
#10
def task_hunansheng(**args):
    conp=get_conp(hunansheng._name_)
    hunansheng.work(conp,pageloadtimeout=180,**args)

#11
def task_jiangxisheng(**args):
    conp = get_conp(jiangxisheng._name_)
    jiangxisheng.work(conp, pageloadtimeout=180, **args)



#13
def task_wuxishi(**args):
    conp = get_conp(wuxishi._name_)
    wuxishi.work(conp, pageloadtimeout=180, **args)

#14
def task_zhejiangsheng(**args):
    conp = get_conp(zhejiangsheng._name_)
    zhejiangsheng.work(conp, pageloadtimeout=180, **args)

#15
def task_anhuisheng1(**args):
    conp=get_conp(anhuisheng1._name_)
    anhuisheng1.work(conp, pageloadtimeout=180,**args)

#16
def task_enshizhou(**args):
    conp=get_conp(enshizhou._name_)
    enshizhou.work(conp,pageloadtimeout=180,**args)


#18
def task_hubeisheng(**args):
    conp=get_conp(hubeisheng._name_)
    hubeisheng.work(conp,pageloadtimeout=180,**args)


def task_sichuansheng(**args):
    conp = get_conp(sichuansheng._name_)
    sichuansheng.work(conp, pageloadtimeout=180, **args)


def task_qinghaisheng1(**args):
    conp = get_conp(qinghaisheng1._name_)
    qinghaisheng1.work(conp, pageloadtimeout=180, **args)


def task_neimenggu(**args):
    conp = get_conp(neimenggu._name_)
    neimenggu.work(conp, pageloadtimeout=180, **args)


def task_all():
    bg=time.time()
    try:
        task_ezhoushi()
        task_guizhousheng()
        task_qinghaisheng()
        task_shaoyangxian()
        task_shenzhenshi()
    except:
        print("part1 error!")

    try:
        task_anhuisheng()
        task_guangdongsheng()
        task_guangxisheng()
        task_henansheng()
        task_hunansheng()
    except:
        print("part2 error!")

    try:
        task_jiangxisheng()
        task_wuxishi()
        task_zhejiangsheng()
        task_anhuisheng1()
    except:
        print("part3 error!")

    try:
        task_enshizhou()
        task_hubeisheng()
        task_sichuansheng()
        task_qinghaisheng1()
        task_neimenggu()
    except:
        print("part4 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zlest')
    arr=["ezhoushi", "guizhousheng", "qinghaisheng","shaoyangxian","shenzhenshi",
         "anhuisheng", "guangdongsheng", "guangxisheng", "henansheng", "hunansheng",
         "jiangxisheng", "wuxishi", "zhejiangsheng","anhuisheng1",
         "enshizhou","hubeisheng","sichuansheng","qinghaisheng1","neimenggu"]
    for diqu in arr:
        sql="create schema if not exists %s"% (diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




