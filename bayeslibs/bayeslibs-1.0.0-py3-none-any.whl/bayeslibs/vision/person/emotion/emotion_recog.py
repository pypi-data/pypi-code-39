# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import emotion_recog_bridge
from bayeslibs.config import const


class ApolloEmotionRecognizer:
    """
    表情识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open(is_show=True):
        return open_emotion_recognizer(is_show)

    @staticmethod
    def close():
        return close_emotion_recognizer()

    @staticmethod
    def emotions():
        return get_emotions_recognized()


def open_emotion_recognizer(is_show=True):
    """
    开启机器人表情识别功能
    :param
    :return:result
    :example:
        result = open_emotion_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = emotion_recog_bridge(req_type=const.TYPE_START, is_show=is_show)
    return result


def close_emotion_recognizer():
    """
    关闭机器人表情识别功能
    :param
    :return:result
    :example:
        result = close_emotion_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = emotion_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_emotions_recognized():
    """
    查询机器人表情识别出的人脸信息
    :return:result
    :example:
        result = get_emotions_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                    'emotion':'happy',
                    'score':88,
                    'width':123,
                    'height':223,
                    'top':12,
                    'left':33
                 },
                 ...
            ]
        }
    """
    result = emotion_recog_bridge(req_type=const.TYPE_QUERY)
    return result
