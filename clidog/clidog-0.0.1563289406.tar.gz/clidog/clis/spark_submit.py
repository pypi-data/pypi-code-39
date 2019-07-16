#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-CLI.
# @File         : spark_submit
# @Time         : 2019-07-16 16:50
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 
import yaml
import os


def spark_submit(config="/Users/yuanjie/Desktop/Projects/Python/tql-CLI/clidog/clis/spark_submit.yml", **kwargs):
    """

    :param config: 配置文件
    :param kwargs:
    :return:
        ~/infra-client/bin/spark-submit
        --name SparkApp
        --cluster zjyprc-hadoop
        --master yarn-cluster
        --queue production.miui_group.browser.miui_browser_zjy_1
        --num-executors 64
        --executor-cores 2
        --executor-memory 6g
        --driver-memory 6g
        --conf spark.yarn.job.owners=yuanjie
        --conf spark.yarn.alert.phone.number=18550288233
        --conf spark.yarn.alert.mail.address=yuanjie@xiaomi.com
        --conf spark.driver.maxResultSize=4g
        --conf spark.sql.catalogImplementation=in-memory
        --class WordVectorTrain
         Spark-Nanjing-1.0-SNAPSHOT.jar
    """
    if os.path.exists(config):
        with open(config) as f:
            config = yaml.safe_load(f)
    config = config if config else {}
    opt = {**config, **kwargs}
    # print(opt)

    cmd = f"""
            ~/infra-client/bin/spark-submit
            --name {opt.get('name', 'SparkApp')}
            --cluster {opt.get('cluster', 'zjyprc-hadoop')}
            --master {opt.get('master', 'yarn-cluster')}
            --queue {opt.get('queue', 'production.miui_group.browser.miui_browser_zjy_1')}
            --num-executors {opt.get('num_executors', 8)}
            --executor-cores {opt.get('executor_cores', 2)}
            --executor-memory {opt.get('executor_memory', '6g')}
            --driver-memory {opt.get('driver_memory', '6g')}
            --conf spark.yarn.job.owners={opt.get('owners')}
            --conf spark.yarn.alert.phone.number={opt.get('phone')}
            --conf spark.yarn.alert.mail.address={opt.get('mail')}
            --conf spark.driver.maxResultSize=4g
            --conf spark.sql.catalogImplementation=in-memory
            --class {opt.get('main_class')}
             {opt.get('jar', 'Spark-Nanjing-1.0-SNAPSHOT.jar')}
            """
    print(cmd)
    os.popen(cmd.replace('\n', ' ')).read()


# class SparkSubmit(object):
#
#     def __init__(self, config="/Users/yuanjie/Desktop/Projects/Python/tql-CLI/clidog/clis/spark_submit.yml", **kwargs):
#         with open(config) as f:
#             cfg = {**yaml.safe_load(f), **kwargs}
#         print(cfg)
#         for k, v in cfg.items():
#             setattr(self, k, v)
#
#         cmd = f"""
#                 ~/infra-client/bin/spark-submit
#                 --name {self.name}
#                 --cluster {self.cluster}
#                 --master yarn-cluster
#                 --queue {self.queue}
#                 --num-executors {self.num_executors}
#                 --executor-cores {self.executor_cores}
#                 --executor-memory {self.executor_memory}
#                 --driver-memory {self.driver_memory}
#                 --conf spark.yarn.job.owners={self.owners}
#                 --conf spark.yarn.alert.phone.number={self.phone}
#                 --conf spark.yarn.alert.mail.address={self.mail}
#                 --conf spark.driver.maxResultSize=4g
#                 --conf spark.sql.catalogImplementation=in-memory
#                 --class {self.main_class}
#                 {self.jar}
#                 """
#         print(cmd)
#         os.popen(cmd).read()
if __name__ == '__main__':
    spark_submit()
