import time

from zlest.bc_diqu import bc_ezhou
from zlest.bc_diqu import bc_guizhou
from zlest.bc_diqu import bc_qinghai
from zlest.bc_diqu import bc_shaoyang
from zlest.bc_diqu import bc_shenzhen

from zlest.bc_diqu import bc_anhui
from zlest.bc_diqu import bc_guangdong
from zlest.bc_diqu import bc_guangxi
from zlest.bc_diqu import bc_henan
from zlest.bc_diqu import bc_hunan


from zlest.bc_diqu import bc_jiangxi
from zlest.bc_diqu import bc_qg_ggzy
from zlest.bc_diqu import bc_wuxi
from zlest.bc_diqu import bc_zhejiang
from zlest.bc_diqu import bc_anhui1

from zlest.bc_diqu import bc_enshi
from zlest.bc_diqu import bc_qg_zfcg
from zlest.bc_diqu import bc_hubei


from lmf.dbv2 import db_command

from zlest.util.conf import get_conp,get_conp1

#1
def task_ezhou(**args):
    conp=get_conp(bc_ezhou._name_)
    bc_ezhou.work(conp,pageloadtimeout=180,**args)

#2
def task_guizhou(**args):
    conp=get_conp(bc_guizhou._name_)
    bc_guizhou.work(conp,pageloadtimeout=180,**args)

#3
def task_qinghai(**args):
    conp=get_conp(bc_qinghai._name_)
    bc_qinghai.work(conp,pageloadtimeout=180,**args)

#4
def task_shaoyang(**args):
    conp=get_conp(bc_shaoyang._name_)
    bc_shaoyang.work(conp,pageloadtimeout=180,**args)

#5
def task_shenzhen(**args):
    conp=get_conp(bc_shenzhen._name_)
    bc_shenzhen.work(conp,pageloadtimeout=180,**args)
#6
def task_anhui(**args):
    conp=get_conp(bc_anhui._name_)
    bc_anhui.work(conp,pageloadtimeout=180,**args)
#7
def task_guangdong(**args):
    conp=get_conp(bc_guangdong._name_)
    bc_guangdong.work(conp,pageloadtimeout=180,**args)
#8
def task_guangxi(**args):
    conp=get_conp(bc_guangxi._name_)
    bc_guangxi.work(conp,pageloadtimeout=180,**args)
#9
def task_henan(**args):
    conp=get_conp(bc_henan._name_)
    bc_henan.work(conp,pageloadtimeout=180,**args)
#10
def task_hunan(**args):
    conp=get_conp(bc_hunan._name_)
    bc_hunan.work(conp,pageloadtimeout=180,**args)

#11
def task_jiangxi(**args):
    conp = get_conp(bc_jiangxi._name_)
    bc_jiangxi.work(conp, pageloadtimeout=180, **args)

#12
def task_qg_ggzy(**args):
    conp = get_conp(bc_qg_ggzy._name_)
    bc_qg_ggzy.work(conp, pageloadtimeout=180, **args)

#13
def task_wuxi(**args):
    conp = get_conp(bc_wuxi._name_)
    bc_wuxi.work(conp, pageloadtimeout=180, **args)

#14
def task_zhejiang(**args):
    conp = get_conp(bc_zhejiang._name_)
    bc_zhejiang.work(conp, pageloadtimeout=180, **args)

#15
def task_anhui1(**args):
    conp=get_conp(bc_anhui1._name_)
    bc_anhui1.work(conp,pageloadtimeout=180,**args)

#16
def task_enshi(**args):
    conp=get_conp(bc_enshi._name_)
    bc_enshi.work(conp,pageloadtimeout=180,**args)

#17
def task_qg_zfcg(**args):
    conp = get_conp(bc_qg_zfcg._name_)
    bc_qg_zfcg.work(conp, pageloadtimeout=180, **args)

#18
def task_hubei(**args):
    conp=get_conp(bc_hubei._name_)
    bc_hubei.work(conp,pageloadtimeout=180,**args)



def task_all():
    bg=time.time()
    try:
        task_ezhou()
        task_guizhou()
        task_qinghai()
        task_shaoyang()
        task_shenzhen()
    except:
        print("part1 error!")

    try:
        task_anhui()
        task_guangdong()
        task_guangxi()
        task_henan()
        task_hunan()
    except:
        print("part2 error!")

    try:
        task_jiangxi()
        task_qg_ggzy()
        task_wuxi()
        task_zhejiang()
        task_anhui1()
    except:
        print("part3 error!")

    try:
        task_enshi()
        task_qg_zfcg()
        task_hubei()
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
         "enshizhou","qg_zfcg","hubeisheng"]
    for diqu in arr:
        sql="create schema if not exists %s"% ('bc__'+diqu)
        db_command(sql,dbtype="postgresql",conp=conp)




