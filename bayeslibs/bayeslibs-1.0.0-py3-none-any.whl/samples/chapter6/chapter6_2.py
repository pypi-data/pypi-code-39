# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from abc import abstractmethod

from bayeslibs.motion import get_robot_rotate_status, robot_rotate_right, robot_rotate_left


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


def apollo_rotate_sample(motion_type, para):
    """
    自定义角度，让小车实现旋转运动
    :param motion_type:向左转、前右转
    :param para:
    :return:
    """
    if motion_type == '向右转':
        # 初始化Apollo转动模块实例
        apollo_move = ApolloRotateRight()
        print('------------------------------------')
        print('发送向右转{}度的运动指令'.format(para))
        apollo_move.rotate(para)  # # 向右转**度
        return True
    elif motion_type == '向左转':
        # 初始化Apollo转动模块实例
        apollo_move = ApolloRotateLeft()
        print('------------------------------------')
        print('发送向左转{}度的运动指令'.format(para))
        apollo_move.rotate(para)  # # 向左转**度
        return True
    else:
        print('------------------------------------')
        print('输入参数有误，请重新输入')
        return False


if __name__ == '__main__':
    count = 0
    # 程序运行10次，次数可修改
    # 运动指令：向右转，向左转
    # 运动参数：10,30,60,90等角度
    while count < 10:
        motion_type_ = input('请输入运动指令:')
        para_ = float(input('请输入运动参数:'))
        apollo_rotate_sample(motion_type_, para_)
        count += 1
