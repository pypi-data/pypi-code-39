import time

from zlest.bc_diqu import bc_ezhoushi
from zlest.bc_diqu import bc_guizhousheng
from zlest.bc_diqu import bc_qinghaisheng
from zlest.bc_diqu import bc_shaoyangxian
from zlest.bc_diqu import bc_shenzhenshi

from zlest.bc_diqu import bc_anhuisheng
from zlest.bc_diqu import bc_guangdongsheng
from zlest.bc_diqu import bc_guangxisheng
from zlest.bc_diqu import bc_henansheng
from zlest.bc_diqu import bc_hunansheng


from zlest.bc_diqu import bc_jiangxisheng
from zlest.bc_diqu import bc_qg_ggzy
from zlest.bc_diqu import bc_wuxishi
from zlest.bc_diqu import bc_zhejiangsheng
from zlest.bc_diqu import bc_anhuisheng1

from zlest.bc_diqu import bc_enshizhou
from zlest.bc_diqu import bc_qg_zfcg
from zlest.bc_diqu import bc_hubeisheng
from zlest.bc_diqu import bc_sichuansheng
from zlest.bc_diqu import bc_qinghaisheng1
from zlest.bc_diqu import bc_neimenggu



from lmf.dbv2 import db_command

from zlest.util.conf import get_conp,get_conp1

#1
def task_bc_ezhoushi(**args):
    conp=get_conp(bc_ezhoushi._name_)
    bc_ezhoushi.work(conp,pageloadtimeout=180,**args)

#2
def task_bc_guizhousheng(**args):
    conp=get_conp(bc_guizhousheng._name_)
    bc_guizhousheng.work(conp,pageloadtimeout=180,**args)

#3
def task_bc_qinghaisheng(**args):
    conp=get_conp(bc_qinghaisheng._name_)
    bc_qinghaisheng.work(conp,pageloadtimeout=180,**args)

#4
def task_bc_shaoyangxian(**args):
    conp=get_conp(bc_shaoyangxian._name_)
    bc_shaoyangxian.work(conp,pageloadtimeout=180,**args)

#5
def task_bc_shenzhenshi(**args):
    conp=get_conp(bc_shenzhenshi._name_)
    bc_shenzhenshi.work(conp,pageloadtimeout=180,**args)
#6
def task_bc_anhuisheng(**args):
    conp=get_conp(bc_anhuisheng._name_)
    bc_anhuisheng.work(conp,pageloadtimeout=180,**args)
#7
def task_bc_guangdongsheng(**args):
    conp=get_conp(bc_guangdongsheng._name_)
    bc_guangdongsheng.work(conp,pageloadtimeout=180,**args)
#8
def task_bc_guangxisheng(**args):
    conp=get_conp(bc_guangxisheng._name_)
    bc_guangxisheng.work(conp,pageloadtimeout=180,**args)
#9
def task_bc_henansheng(**args):
    conp=get_conp(bc_henansheng._name_)
    bc_henansheng.work(conp,pageloadtimeout=180,**args)
#10
def task_bc_hunansheng(**args):
    conp=get_conp(bc_hunansheng._name_)
    bc_hunansheng.work(conp,pageloadtimeout=180,**args)

#11
def task_bc_jiangxisheng(**args):
    conp = get_conp(bc_jiangxisheng._name_)
    bc_jiangxisheng.work(conp, pageloadtimeout=180, **args)

#12
def task_bc_qg_ggzy(**args):
    conp = get_conp(bc_qg_ggzy._name_)
    bc_qg_ggzy.work(conp, pageloadtimeout=180, **args)

#13
def task_bc_wuxishi(**args):
    conp = get_conp(bc_wuxishi._name_)
    bc_wuxishi.work(conp, pageloadtimeout=180, **args)

#14
def task_bc_zhejiangsheng(**args):
    conp = get_conp(bc_zhejiangsheng._name_)
    bc_zhejiangsheng.work(conp, pageloadtimeout=180, **args)

#15
def task_bc_anhuisheng1(**args):
    conp=get_conp(bc_anhuisheng1._name_)
    bc_anhuisheng1.work(conp,pageloadtimeout=180,**args)

#16
def task_bc_enshizhou(**args):
    conp=get_conp(bc_enshizhou._name_)
    bc_enshizhou.work(conp,pageloadtimeout=180,**args)

#17
def task_bc_qg_zfcg(**args):
    conp = get_conp(bc_qg_zfcg._name_)
    bc_qg_zfcg.work(conp, pageloadtimeout=180, **args)

#18
def task_bc_hubeisheng(**args):
    conp=get_conp(bc_hubeisheng._name_)
    bc_hubeisheng.work(conp,pageloadtimeout=180,**args)


def task_bc_sichuansheng(**args):
    conp = get_conp(bc_sichuansheng._name_)
    bc_sichuansheng.work(conp, pageloadtimeout=180, **args)


def task_bc_qinghaisheng1(**args):
    conp = get_conp(bc_qinghaisheng1._name_)
    bc_qinghaisheng1.work(conp, pageloadtimeout=180, **args)


def task_bc_neimenggu(**args):
    conp = get_conp(bc_neimenggu._name_)
    bc_neimenggu.work(conp, pageloadtimeout=180, **args)


def task_all():
    bg=time.time()
    try:
        task_bc_ezhoushi()
        task_bc_guizhousheng()
        task_bc_qinghaisheng()
        task_bc_shaoyangxian()
        task_bc_shenzhenshi()
    except:
        print("part1 error!")

    try:
        task_bc_anhuisheng()
        task_bc_guangdongsheng()
        task_bc_guangxisheng()
        task_bc_henansheng()
        task_bc_hunansheng()
    except:
        print("part2 error!")

    try:
        task_bc_jiangxisheng()
        task_bc_qg_ggzy()
        task_bc_wuxishi()
        task_bc_zhejiangsheng()
        task_bc_anhuisheng1()
    except:
        print("part3 error!")

    try:
        task_bc_enshizhou()
        task_bc_qg_zfcg()
        task_bc_hubeisheng()
        task_bc_sichuansheng()
        task_bc_qinghaisheng1()
        task_bc_neimenggu()
    except:
        print("part4 error!")

    ed=time.time()
    cos=int((ed-bg)/60)
    print("共耗时%d min"%cos)


def create_schemas():
    conp=get_conp1('zlest')
    arr=["ezhoushi", "guizhousheng", "qinghaisheng","shaoyangxian","shenzhenshi",
         "anhuisheng", "guangdongsheng", "guangxisheng", "henansheng", "hunansheng",
         "jiangxisheng", "qg_ggzy", "wuxishi", "zhejiangsheng","anhuisheng1",
         "enshizhou","qg_zfcg","hubeisheng","sichuansheng","qinghaisheng1","neimenggu"]
    for diqu in arr:
        sql="create schema if not exists %s"% (diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




