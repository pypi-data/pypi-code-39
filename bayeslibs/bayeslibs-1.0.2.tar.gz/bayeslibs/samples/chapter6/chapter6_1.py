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


def apollo_move_sample(motion_type, para):
    """
    自定义距离，让小车实现直线运动
    :param motion_type: 向前走，向后走
    :param para: 1.5
    :return:
    """
    if motion_type == '向前走':
        # 初始化Apollo运动模块实例
        apollo_move = ApolloMoveForward()
        print('------------------------------------')
        print('发送向前走{}m的运动指令'.format(para))
        apollo_move.move(para)  # 向前走**m
        return True
    elif motion_type == '向后走':
        # 初始化Apollo运动模块实例
        apollo_move = ApolloMoveBack()
        print('------------------------------------')
        print('发送向后走{}m的运动指令'.format(para))
        apollo_move.move(para)  # 向前走**m
        return True
    else:
        print('------------------------------------')
        print('输入参数有误，请重新输入')
        return False


if __name__ == '__main__':
    count = 0
    # 程序运行10次，次数可修改
    # 运动指令：向前走，向后走
    # 运动参数：1,1.4,2,3,不要超过10m
    while count < 10:
        motion_type_ = input('请输入运动指令:')
        para_ = float(input('请输入运动参数:'))
        apollo_move_sample(motion_type_, para_)
        count += 1
