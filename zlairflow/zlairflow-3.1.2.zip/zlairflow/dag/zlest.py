import sys
import os
from zlairflow.dag.data.data_zlest import para


def write_dag(quyu, dirname, **krg):
    para = {
        "tag": "cdc",
        "start_date": "(2019,5,18)",
        "cron": "0 0/12 * * *",
        "timeout": 'minutes=120'
    }
    para.update(krg)
    tag = para["tag"]
    start_date = para["start_date"]

    cron = para["cron"]

    timeout = para["timeout"]

    arr = quyu.split("_")
    db, schema = arr[0], '_'.join(arr[1:])
    sheng, shi = schema.split("_")[0], '_'.join(schema.split("_")[1:])

    filename = "v5_%s.py" % quyu
    path1 = os.path.join(os.path.dirname(__file__), 'template', 'zlest.txt')
    path2 = os.path.join(dirname, filename)

    with open(path1, 'r', encoding='utf8') as f:
        content = f.read()

    # from ##zhulong.anqing## import ##task_anqing##

    content = content.replace("##task_anqing##", quyu)

    # tag='##cdc##'
    # datetime##(2019,4,27)##, }
    content = content.replace("##cdc##", tag)
    content = content.replace("##(2019,4,27)##", start_date)

    """
    d = DAG('##abc_anhui_anqing##'
            , default_args=default_args
            , schedule_interval="##0 0/12 * * *##"
            ,max_active_runs=1) 
    """
    content = content.replace("##v2_zfcg_anhui_anqing##", "v5_%s" % quyu)

    content = content.replace("##0 0/12 * * *##", cron)

    # task_id="##anqing_a1##"

    content = content.replace("##zfcg_anhui_anqing_a1##", "%s_a1" % quyu)

    content = content.replace("##minutes=60##", timeout)

    content = content.replace("##zfcg_anhui_anqing_b1##", "%s_b1" % quyu)

    content = content.replace("##zfcg_anhui_anqing##", quyu)

    with open(path2, 'w', encoding='utf-8') as f:
        f.write(content)


# write_dag('zfcg_fujian_fuqing',sys.path[0])

def write_dags(dirname, **krg):
    for w in para:
        quyu = '_'.join(w[:2])
        timeout = w[2]
        krg.update({"timeout": timeout})
        write_dag(quyu, dirname, **krg)

# write_dag('zfcg_guandong_dongguan',r'C:\Users\jacky\Desktop\zhulongall\zlairflow\zlairflow\data',start_date='(2019,6,17)',tiemout='minutes=120')