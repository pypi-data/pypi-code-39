import datetime
import logging

from logger.Config import Config

'''
打印log
将原log信息的KV进行过滤，将制定的KV写入固定路径log文件。
随后push到es中，供ai_platform展示使用。
'''


def print_log(value, label):
    if label is None:
        return

    str_value = str(value)
    kv_list = str_value.split("|")
    message = datetime.datetime.now().strftime('%Y-%m-%d')
    for kv in kv_list:
        if kv.__contains__(label):
            message += (" | " + kv)
    logging.info(message)


def init_config():
    Config().config_log()
