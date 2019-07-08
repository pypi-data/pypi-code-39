# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.vbridge import tts_bridge
from bayeslibs.config import const


class ApolloSpeaker:
    """
    语音合成模块封装类
    """

    def __init__(self):
        pass

    @staticmethod
    def stop():
        return stop_speak()

    @staticmethod
    def speak(text):
        return start_speak(text)

    @staticmethod
    def status():
        return get_speak_status()


def start_speak(text):
    """
    机器人播放具体文本语音
    :param text
    :return:result
    :example:
        result = start_speak('今天心情很好')
        ------
        result:{
            'status':0,
            'msg':'start tts success'
        }
    """
    result = tts_bridge(req_type=const.TYPE_START, text=text)
    return result


def stop_speak():
    """
    关闭机器人语音合成
    :param
    :return:result
    :example:
        result = stop_speak()
        ------
        result:{
            'status':0,
            'msg':'stop success'
        }
    """
    result = tts_bridge(req_type=const.TYPE_STOP)
    return result


def get_speak_status():
    """
    查询机器人语音播放状态
    :param
    :return:result
    :example:
        result = get_speak_status()
        ------
        result:{
            'status':0,
            'msg':'voice is playing'
        }
    """
    result = tts_bridge(req_type=const.TYPE_QUERY)
    return result
