# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.ibridge import skeleton_recog_bridge
from bayeslibs.config import const


class ApolloSkeletonRecognizer:
    """
    年龄性别识别模块封装类
    """
    def __init__(self):
        pass

    @staticmethod
    def open():
        return open_skeleton_recognizer()

    @staticmethod
    def close():
        return close_skeleton_recognizer()

    @staticmethod
    def get_face_recognized():
        return get_skeletons_recognized()


def open_skeleton_recognizer():
    """
    开启机器人骨骼识别功能
    :param
    :return:result
    :example:
        result = open_skeleton_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = skeleton_recog_bridge(req_type=const.TYPE_START)
    return result


def close_skeleton_recognizer():
    """
    关闭机器人骨骼识别功能
    :param
    :return:result
    :example:
        result = close_skeleton_recognizer()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = skeleton_recog_bridge(req_type=const.TYPE_STOP)
    return result


def get_skeletons_recognized():
    """
    查询机器人识别出的骨骼信息
    :return:result
    :example:
        result = get_skeletons_recognized()
        ------
        result:{
            'status':0,
            'msg':'success',
            'data':[
                 {
                   'body_parts':[
                        {
                           'points_name':'neck',
                           'x':232,
                           'y':321
                        },
                        {
                           'points_name':'left_shoulder',
                           'x':132,
                           'y':321
                        },
                        {...}
                   ]
                   'width':123,
                   'height':223,
                   'top':12,
                   'left':33
                 },
                 {...}
            ]
        }
    """
    result = skeleton_recog_bridge(req_type=const.TYPE_QUERY)
    return result


if __name__ == '__main__':
    # open_skeleton_recognizer()
    close_skeleton_recognizer()
