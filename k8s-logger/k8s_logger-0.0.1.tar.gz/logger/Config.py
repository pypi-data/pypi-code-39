import logging
import os


class Config:
    '''
        配置log路径
    '''

    def __init__(self):
        self.__log_path = os.getenv("logPath")
        self.__job_name = os.getenv("jobName")

    def config_log(self, log_path=None):
        if log_path is None:
            log_path = os.path.join(self.__log_path, self.__job_name + ".log")

        print("logging init log_path:[%s] " % log_path)
        logging.basicConfig(
            level=logging.DEBUG,
            format='%(asctime)s-%(levelname)s-%(message)s',
            filename=log_path,
            datefmt='%Y-%m-%d %H:%M',
            filemode='a')
