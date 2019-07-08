# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/6/12
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.utils.bridge.vbridge import music_bridge
from bayeslibs.config import const


class ApolloMusicPlayer:
    def __init__(self, music_name):
        self.music_name = music_name

    def play(self):
        return start_music(self.music_name)

    @staticmethod
    def stop():
        return stop_music()

    @staticmethod
    def status():
        return get_music_status()


def start_music(text):
    """
    机器人播放具体音乐
    :param text
    :return:result
    :example:
        result = start_music('钢琴曲')
        ------
        result:{
            'status':0,
            'msg':'start music success'
        }
    """
    result = music_bridge(req_type=const.TYPE_START, text=text)
    return result


def stop_music():
    """
    关闭机器人音乐播放
    :param
    :return:result
    :example:
        result = stop_music()
        ------
        result:{
            'status':0,
            'msg':'success'
        }
    """
    result = music_bridge(req_type=const.TYPE_STOP)
    return result


def get_music_status():
    """
    查询机器人音乐播放状态
    :param
    :return:result
    :example:
        result = get_music_status()
        ------
        result:{
            'status':0,
            'msg':'voice is playing'
        }
    """
    result = music_bridge(req_type=const.TYPE_QUERY)
    return result
