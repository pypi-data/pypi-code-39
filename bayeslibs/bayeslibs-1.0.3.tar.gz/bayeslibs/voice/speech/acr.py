# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/26
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.vbridge import acr_bridge
from bayeslibs.config import const


class ApolloACRer:
    """
    语音识别模块封装类
    """

    def __init__(self):
        pass

    @staticmethod
    def open():
        return open_acr()

    @staticmethod
    def close():
        return close_acr()

    @staticmethod
    def status():
        return get_acr_status()


def open_acr():
    """
    开启机器人命令词识别
    :param:
    :return:result
    :example:
        result = open_acr()
        ------
        result:{
            'status':0,
            'msg':'start acr success'
        }
    """
    result = acr_bridge(req_type=const.TYPE_START)
    return result


def close_acr():
    """
    关闭机器人命令词识别
    :param
    :return:result
    :example:
        result = close_acr()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = acr_bridge(req_type=const.TYPE_STOP)
    return result


def get_acr_status():
    """
    查询命令词识别状态
    :param
    :return:result
    :example:
        result = get_acr_status()
        ------
        result:{
            'status':0,
            'msg':'success',
            'text':'向前走2米',
            'is_asr':true
        }
    """
    result = acr_bridge(req_type=const.TYPE_QUERY)
    return result
