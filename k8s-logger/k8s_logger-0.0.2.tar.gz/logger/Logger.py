import datetime
import logging
from functools import reduce

from logger.Config import Config

'''
打印log
将原log信息的KV进行过滤，将制定的KV写入固定路径log文件。
随后push到es中，供ai_platform展示使用。
'''


def print_log(value, *args):
    if args is None:
        return

    __labels = {"epoch", "iter", "speed"}

    __labels = __labels | set(args)

    kv_list = str(value).split("|")
    message = datetime.datetime.now().strftime('%Y-%m-%d') + " "

    def filter_kv(kv):
        def reduce_kv(result, label):
            if not isinstance(result, bool):
                result = True if str(kv).__contains__(result) else False

            return result or (True if kv.__contains__(label) else False)

        return reduce(reduce_kv, __labels)

    # 对kv_list进行过滤。过滤后的结果进行拼接打印
    # 对每一个kv 与__labels进行对比。含有某个label 则保留
    log_result = list(filter(filter_kv, kv_list))
    logging.info(message + reduce(lambda result, log_txt: result + " | " + log_txt, log_result))


def init_config():
    Config().config_log()
