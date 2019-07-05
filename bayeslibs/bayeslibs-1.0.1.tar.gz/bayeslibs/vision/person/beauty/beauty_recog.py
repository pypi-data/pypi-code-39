# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import beauty_recog_bridge
from bayeslibs.config import const


class ApolloBeautyAgeGenderRecognizer:
    """
    年龄性别识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open():
        return open_beauty_age_gender_recognizer()

    @staticmethod
    def close():
        return close_beauty_age_gender_recognizer()

    @staticmethod
    def beauties():
        return get_beauty_age_genders_recognized()


def open_beauty_age_gender_recognizer(is_show=True):
    """
    开启机器人颜值年龄性别识别功能
    :param
    :return:result
    :example:
        result = open_beauty_age_gender_recognizer(True)
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = beauty_recog_bridge(req_type=const.TYPE_START, is_show=is_show)
    return result


def close_beauty_age_gender_recognizer():
    """
    关闭机器人颜值年龄性别识别功能
    :param
    :return:result
    :example:
        result = close_beauty_age_gender_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = beauty_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_beauty_age_genders_recognized():
    """
    查询机器人识别出的颜值年龄性别信息
    :return:result
    :example:
        result = get_beauty_age_genders_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                    'beauty':40,
                    'gender':'male',
                    'gender_confidence':0.98,
                    'age': 27,
                    'width':123,
                    'height':223,
                    'top':12,
                    'left':33
                 },
                 ...
            ]
        }
    """
    result = beauty_recog_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    open_beauty_age_gender_recognizer(True)
    # close_beauty_recognizer()
