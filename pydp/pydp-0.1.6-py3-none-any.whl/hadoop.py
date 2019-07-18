#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
File: hadoop.py
Desc: hadoop操作封装
Author:yanjingang(yanjingang@mail.com)
Date: 2019/2/21 23:34
"""

import os
import sys
import logging
import subprocess
from dp import utils,constants

class Hadoop():
    """hadoop集群交互封装"""

    def __init__(self, bin_path):
        """
        初始化

        :param bin_path: hadoop client文件（例：/home/work/hadoop-client/bin/hadoop）
        :returns: 
        """
        self.HADOOP_BIN = bin_path

    def exec_cmd(self, cmd):
        """
        执行命令

        :param cmd: shell 命令
        :returns: [status(0成功，非0失败), info]
        """
        logging.info("[Hadoop]exec cmd: " + cmd)
        return subprocess.getstatusoutput(cmd)

    def ls(self, hdfs_path):
        """
        获取hdfs目录下信息

        :param hdfs_path: 远端hadoop集群path目录
        :returns: 目录信息
        """
        cmd = self.HADOOP_BIN + ' fs -ls ' + hdfs_path
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]show hdfs path info failed! [" + cmd + "][" + str(info) + "]")
        # format
        log,info = info.split('items',2)
        res = []
        for row in info.strip().split('\n'):
            cdata = []
            for col in row.strip().split(' '):
                if col != '':
                    cdata.append(col)
            res.append(cdata)
        return res

    def exists(self, hdfs_path):
        """
        检查hdfs路径是否存在

        :param hdfs_path: 远端hadoop集群path目录
        :returns: 是否存在（0存在，非0不存在）
        """
        cmd = self.HADOOP_BIN + ' fs -test -e ' + hdfs_path
        status, info = self.exec_cmd(cmd)
        return status

    def mkdir(self, hdfs_path):
        """
        创建hdfs路径

        :param hdfs_path: 远端hadoop集群path目录
        :returns: 是否成功（0成功，非0失败）
        """
        status = self.exists(hdfs_path)
        if status == 0:
            logging.warning("[Hadoop]hdfs path has exist !")
            return status
        cmd = self.HADOOP_BIN + ' fs -mkdir ' + hdfs_path
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]create hdfs path failed! [" + cmd + "][" + str(info) + "]")
        return status

    def put(self, local_src, hdfs_dest):
        """
        将本地文件上传到hdfs指定路径下

        :param local_src: 本地文件或目录
        :param hdfs_dest: 远端hadoop集群位置
        :returns: 是否成功（0成功，非0失败）
        """
        flag = self.exists(hdfs_dest)
        if flag != 0:
            ret = self.mkdir(hdfs_dest)
            if ret != 0:
                return ret
        cmd = self.HADOOP_BIN + ' fs -put ' + local_src + ' ' + hdfs_dest
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]upload local file to hdfs failed! [" + cmd + "][" + str(info) + "]")
        return status

    def get(self, hdfs_src, local_dest):
        """
        将hdfs文件下载到本地

        :param hdfs_src: 远端hadoop集群文件或目录
        :param local_dest: 下载到本地位置
        :returns: 是否成功（0成功，非0失败）
        """
        #utils.mv(local_dest, local_dest + '.bak')
        cmd = self.HADOOP_BIN + ' fs -get ' + hdfs_src + ' ' + local_dest
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]download hdfs file failed! [" + cmd + "][" + str(info) + "]")
        return status

    def getmerge(self, hdfs_path, local_dest):
        """
        将hdfs路径下所有文件合并后下载到本地

        :param hdfs_path: 远端hadoop集群目录
        :param local_dest: 下载到本地位置
        :returns: 是否成功（0成功，非0失败）
        """
        #utils.mv(local_dest, local_dest + '.bak')
        cmd = self.HADOOP_BIN + ' fs -getmerge ' + hdfs_path + ' ' + local_dest
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]download hdfs file failed! [" + cmd + "][" + str(info) + "]")
        return status

    def rmr(self, hdfs_path):
        """
        删除hadoop上面的路径或文件

        :param hdfs_path: 远端hadoop集群目录或文件
        :returns: 是否成功（0成功，非0失败）
        """
        cmd = self.HADOOP_BIN + ' fs -rmr ' + hdfs_path
        status, info = self.exec_cmd(cmd)
        if status != 0:
            logging.error("[Hadoop]remove hdfs file failed! [" + cmd + "][" + str(info) + "]")
        return status


if __name__ == '__main__':
    """test"""
    hadoop = Hadoop("/home/work/hadoop-client-all/hadoop-client-zhixin/hadoop/bin/hadoop")
    res = hadoop.exists('/user/zhixin/aladdin/yanjingang/test')
    print("hadoop.exists: {}".format(res))
    res = hadoop.rmr('/user/zhixin/aladdin/yanjingang/test')
    print("hadoop.rmr: {}".format(res))
    res = hadoop.ls('/user/zhixin/aladdin/yanjingang/')
    print("hadoop.ls: {}".format(res))
    res = hadoop.mkdir('/user/zhixin/aladdin/yanjingang/test/')
    print("hadoop.mkdir: {}".format(res))
    res = hadoop.put(__file__, '/user/zhixin/aladdin/yanjingang/test/')
    print("hadoop.put: {}".format(res))
    res = hadoop.ls('/user/zhixin/aladdin/yanjingang/test/')
    print("hadoop.ls: {}".format(res))
    utils.rm(constants.APP_PATH + '/log/hadoop.py')
    res = hadoop.get('/user/zhixin/aladdin/yanjingang/test/hadoop.py',constants.APP_PATH + '/log/hadoop.py')
    print("hadoop.get: {}".format(res))
    utils.rmdir(constants.APP_PATH + '/log/test/')
    res = hadoop.get('/user/zhixin/aladdin/yanjingang/test',constants.APP_PATH + '/log/test')
    print("hadoop.get path: {}".format(res))
