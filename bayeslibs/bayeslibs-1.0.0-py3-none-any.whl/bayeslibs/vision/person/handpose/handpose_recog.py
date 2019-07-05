# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import handpose_recog_bridge
from bayeslibs.config import const


class ApolloHandPoseRecognizer:
    """
    年龄性别识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open():
        return open_handpose_recognizer()

    @staticmethod
    def close():
        return close_handpose_recognizer()

    @staticmethod
    def handposes():
        return get_handposes_recognized()


def open_handpose_recognizer():
    """
    开启机器人手势识别功能
    :param
    :return:result
    :example:
        result = open_handpose_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = handpose_recog_bridge(req_type=const.TYPE_START)
    return result


def close_handpose_recognizer():
    """
    关闭机器人手势识别功能
    :param
    :return:result
    :example:
        result = close_handpose_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = handpose_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_handposes_recognized():
    """
    查询机器人识别出的手势信息
    :return:result
    :example:
        result = get_handposes_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                   'classname':'Ok',
                   'probability':0.53,
                   'width':123,
                   'height':223,
                   'top':12,
                   'left':33
                 },
                 {...}
            ]
        }
    """
    result = handpose_recog_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    # open_handpose_recognizer()
    close_handpose_recognizer()
