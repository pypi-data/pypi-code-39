from zhulong2.hebei import shenghui
from zhulong2.hebei import tangshan
from zhulong2.hebei import chengde





from lmf.dbv2 import db_command


from os.path import join ,dirname 

import time 

from zhulong2.util.conf import get_conp,get_conp1


#5
def task_shenghui(**args):
    conp=get_conp(shenghui._name_)
    shenghui.work(conp,**args)
#5
def task_tangshan(**args):
    conp=get_conp(tangshan._name_)
    tangshan.work(conp,**args)
#5
def task_chengde(**args):
    conp=get_conp(chengde._name_)
    chengde.work(conp,**args)







def task_all():
    bg = time.time()
    try:
        task_shenghui()
        task_tangshan()
        task_chengde()
    except:
        print("part hebei error!")

    ed = time.time()

    cos = int((ed - bg) / 60)

    print("共耗时%d min" % cos)

def create_schemas():
    conp = get_conp1('zfcg')
    arr = [
        'hebei_shenghui',
        'hebei_tangshan',
        'hebei_chengde',
    ]
    for diqu in arr:
        sql = "create schema if not exists %s" % diqu
        db_command(sql, dbtype="postgresql", conp=conp)
    
