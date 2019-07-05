# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/12
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import color_recog_bridge
from bayeslibs.config import const


class ApolloColorRecognizer:
    """
    颜色识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open(colors):
        return open_single_color_recognizer(colors)

    @staticmethod
    def close():
        return close_color_recognizer()

    @staticmethod
    def colors():
        return get_colors_recognized()


def open_single_color_recognizer(color):
    """
    开启机器人单张色卡颜色识别功能
    :param
    :return:result
    :example:
        result = open_single_color_recognizer('red')
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = color_recog_bridge(req_type=const.TYPE_START, colors=color, is_multi=False)
    return result


def open_multi_color_recognizer(colors):
    """
    开启机器人多张色卡颜色识别功能
    :param
    :return:result
    :example:
        result = open_multi_color_recognizer('red,blue,green')
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = color_recog_bridge(req_type=const.TYPE_START, colors=colors, is_multi=True)
    return result


def close_color_recognizer():
    """
    关闭机器人颜色识别功能
    :param
    :return:result
    :example:
        result = close_color_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = color_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_colors_recognized():
    """
    查询机器人颜色识别出的颜色信息
    :return:result
    :example:
        result = get_colors_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                {
                    'color':'red',
                    'area':2130,
                    'dist':2.2,
                    'width':123,
                    'height':223,
                    'top':12,
                    'left':33
                },
                {...}
            ]
        }
    """
    result = color_recog_bridge(req_type=const.TYPE_QUERY)
    return result
