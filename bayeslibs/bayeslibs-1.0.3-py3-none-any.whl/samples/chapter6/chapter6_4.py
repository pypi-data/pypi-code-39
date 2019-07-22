# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from abc import abstractmethod
from bayeslibs.motion import robot_move_forward, get_robot_move_status, robot_move_back
from bayeslibs.motion import get_robot_rotate_status, robot_rotate_left, robot_rotate_right
from bayeslibs.voice import start_music, stop_music, get_music_status
import time


class ApolloMusicPlayer:
    def __init__(self):
        self.__music_name = None

    def get_music_name(self):
        return self.__music_name

    def set_music_name(self, music_name):
        self.__music_name = music_name

    def play(self):
        start_music(self.__music_name)

    @staticmethod
    def stop():
        stop_music()

    @staticmethod
    def query():
        get_music_status()


class ApolloMoveBase:
    def __init__(self):
        pass

    @staticmethod
    def get_move_status():
        try:
            print('------------------------------------')
            print('运动中.....')
            move_stat = get_robot_move_status()
            while move_stat['status'] != 0:
                if move_stat['status'] == 505:
                    print('运动程序不存在')
                    return False
                move_stat = get_robot_move_status()
            print('------------------------------------')
            print('运动完成.....')
            print('------------------------------------')
            return True
        except Exception as err:
            print('发生未知错误:{}'.format(err))
            return False

    @abstractmethod
    def move(self, distance):
        pass


class ApolloMoveForward(ApolloMoveBase):
    def __init__(self):
        super().__init__()

    def move(self, distance):
        robot_move_forward(distance)
        return self.get_move_status()


class ApolloMoveBack(ApolloMoveBase):
    def __init__(self):
        super().__init__()

    def move(self, distance):
        robot_move_back(distance)
        return self.get_move_status()


class ApolloRotateBase:
    def __init__(self):
        pass

    @staticmethod
    def get_rotate_status():
        try:
            print('------------------------------------')
            print('转动中.....')
            rotate_stat = get_robot_rotate_status()
            while rotate_stat['status'] != 0:
                if rotate_stat['status'] == 505:
                    print('运动程序不存在')
                    return False
                rotate_stat = get_robot_rotate_status()
            print('------------------------------------')
            print('转动完成.....')
            print('------------------------------------')
            return True
        except Exception as err:
            print('发生未知错误:{}'.format(err))
            return False

    @abstractmethod
    def rotate(self, angle):
        pass


class ApolloRotateRight(ApolloRotateBase):
    def __init__(self):
        super().__init__()

    def rotate(self, angle):
        robot_rotate_right(angle)
        return self.get_rotate_status()


class ApolloRotateLeft(ApolloRotateBase):
    def __init__(self):
        super().__init__()

    def rotate(self, angle):
        robot_rotate_left(angle)
        return self.get_rotate_status()


def robot_move_rectangle_sample():
    """
    自定义路线，让APOLLO小车走一个正方形，完成运动后播放歌曲
    向前走0.5m，到达后向右转90度，然后向前走0.5m，到达后向右转90度，接着再向前走0.5m，紧接着转90度，
    最后再向前走0.5m到达起点位置，完成运动后播放歌曲
    :return:
    """
    try:
        # 初始化Apollo运动模块实例
        apollo_move_forward = ApolloMoveForward()
        # 初始化Apollo转动模块实例
        apollo_rotate_right = ApolloRotateRight()
        # 向前走0.5m
        print('向前运动0.5m')
        apollo_move_forward.move(0.5)
        # 向右转90度
        print('向右转动90度')
        apollo_rotate_right.rotate(90)
        # 向前走0.5m
        print('向前运动0.5m')
        apollo_move_forward.move(0.5)
        # 向右转90度
        print('向右转动90度')
        apollo_rotate_right.rotate(90)
        # 向前走0.5m
        print('向前运动0.5m')
        apollo_move_forward.move(0.5)
        # 向右转90度
        print('向右转动90度')
        apollo_rotate_right.rotate(90)
        # 向前走0.5m
        print('向前运动0.5m')
        apollo_move_forward.move(0.5)
        # 向右转90度
        print('向右转动90度')
        apollo_rotate_right.rotate(90)
    except Exception as err:
        print('运动模块发生未知错误:{}'.format(err))
        return
    try:
        # 初始化Apollo音乐模块实例
        apollo_music = ApolloMusicPlayer()
        # 播放音乐：来自天堂的魔鬼
        apollo_music.set_music_name('来自天堂的魔鬼')
        print('播放音乐:{}'.format('来自天堂的魔鬼'))
        apollo_music.play()
        # 暂停40s播放音乐
        time.sleep(40)
        # 关闭音乐播放
        apollo_music.stop()
    except Exception as err:
        print('音乐模块发生未知错误:{}'.format(err))
        return


if __name__ == '__main__':
    # 机器人规则运动
    robot_move_rectangle_sample()
