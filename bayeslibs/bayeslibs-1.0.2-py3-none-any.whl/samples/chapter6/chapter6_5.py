# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from abc import abstractmethod
from bayeslibs.motion import robot_move_forward, get_robot_move_status, robot_move_back
from bayeslibs.motion import robot_rotate_right, robot_rotate_left, stop_robot_rotate
from bayeslibs.motion import stop_robot_move, get_robot_rotate_status
from bayeslibs.voice import open_acr, get_acr_status, get_speak_status
from bayeslibs.voice import open_wakeup, get_wakeup_status
from bayeslibs.voice import start_speak


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


def wakeup():
    """
    唤醒小贝
    """
    open_res = open_wakeup()
    if open_res and open_res['status'] == 0:
        ret = get_wakeup_status()
        print('------------------------------------')
        print('小贝等待唤醒中.......')
        while ret['status'] != 0:
            ret = get_wakeup_status()
        print('------------------------------------')
        print('小贝唤醒成功，唤醒角度:{}'.format(ret['angle']))
        return True
    else:
        return False


def auto_command_recognize():
    """
    APOLLO机器人离线命令词识别
    """
    res_asr = open_acr()
    if res_asr and res_asr['status'] == 0:
        stat = get_acr_status()
        print('------------------------------------')
        print('小贝识别中.......')
        while stat and stat['is_acr']:
            stat = get_acr_status()
        print('------------------------------------')
        if 'text' in stat and stat['text']:
            print('小贝识别成功:{}'.format(stat['text']))
            print('------------------------------------')
            ret = stat['text']
            return True, ret
        else:
            ret = '不好意思，小贝没有听清你的声音'
            return False, ret
    else:
        return False, '网络故障'


def voice_play(text):
    """
       输入任意内容，让APOLLO机器人将其播放出来，实现语音合成功能
    """
    start_res = start_speak(text)
    if start_res and start_res['status'] == 0:
        res = get_speak_status()
        print('------------------------------------')
        print('小贝语音合成中.......')
        while res['status'] == 0:
            res = get_speak_status()
        return True
    else:
        return False


class CommandController:
    __DISTANCE_SUPPORT = [0.5, 1, 1.5, 2, 2.5, 3, 3.5, 4, 4.5, 5]
    __ANGLE_SUPPORT = {'十': 10, '二十': 20, '三十': 30, '四十': 40, '五十': 50,
                       '六十': 60, '七十': 70, '八十': 80, '九十': 90, '一百八十': 180,
                       '二百七十': 270, '三百六十': 360}
    __MSG_REPLY = {'forward': '好的,小贝向前走了',
                   'back': '好的,小贝往后退了',
                   'left': '好的,小贝向左转了',
                   'right': '好的,小贝向右转了',
                   'stop': '好的,小贝不走了'}

    def __init__(self):
        self.m_type = None
        self.m_value = None
        self.mover_f = ApolloMoveForward()
        self.move_b = ApolloMoveBack()
        self.rotate_l = ApolloRotateLeft()
        self.rotate_r = ApolloRotateRight()

    def m_value_attain(self, msg):
        for dist in self.__DISTANCE_SUPPORT:
            if str(dist) in msg:
                return dist
        angle_list = []
        for angle in self.__ANGLE_SUPPORT.keys():
            if angle in msg:
                angle_list.append(angle)
        if len(angle_list) == 1:
            return self.__ANGLE_SUPPORT[angle_list[0]]
        if len(angle_list) == 2:
            angle_list.remove('十')
            return self.__ANGLE_SUPPORT[angle_list[0]]
        return None

    def speak(self):
        print('------------------------------------')
        print(self.__MSG_REPLY[self.m_type])
        voice_play(self.__MSG_REPLY[self.m_type])

    def move_forward(self):
        self.m_type = 'forward'
        self.speak()
        if not self.m_value:
            self.mover_f.move(0.5)
        else:
            self.mover_f.move(self.m_value)

    def move_back(self):
        self.m_type = 'back'
        self.speak()
        if not self.m_value:
            self.move_b.move(0.5)
        else:
            self.move_b.move(self.m_value)

    def rotate_left(self):
        self.m_type = 'left'
        self.speak()
        if not self.m_value:
            self.rotate_l.rotate(90)
        else:
            print(self.m_value)
            self.rotate_l.rotate(self.m_value)

    def rotate_right(self):
        self.m_type = 'right'
        self.speak()
        if not self.m_value:
            self.rotate_r.rotate(90)
        else:
            print(self.m_value)
            self.rotate_r.rotate(self.m_value)

    def stop(self):
        self.speak()
        stop_robot_move()
        stop_robot_rotate()
        self.m_type = 'stop'

    def m_control(self, msg):
        # 提取命令词里的运动参数
        self.m_value = self.m_value_attain(msg)
        # 判断运动类型，并执行相应操作
        if '前' in msg or '前进' in msg or '向前' in msg or '往前' in msg or '前走' in msg:
            self.move_forward()
        elif '后' in msg or '后退' in msg or '向后' in msg or '往后' in msg:
            self.move_back()
        elif '向左' in msg or '往左' in msg or '左转' in msg:
            self.rotate_left()
        elif '向右' in msg or '往右' in msg or '右转' in msg:
            self.rotate_right()
        elif '停止运动' in msg or 'stop' in msg:
            self.stop()
        else:
            print('------------------------------------')
            start_speak('不好意思，小贝没有识别到正确的指令')


def motion_control_by_voice_sample():
    """
    通过语音控制，自定义距离，命令机器人向前/向后/左转/右转运动
    :return:
    """
    # 首先进行语音唤醒
    w_res = wakeup()
    if not w_res:
        print('小贝唤醒失败，请监测网络设备')
        return False
    # 唤醒成功后进行语音识别
    ret, msg = auto_command_recognize()
    if not ret:
        print('小贝识别失败，请重新唤醒和识别')
        return False
    print('------------------------------------')
    print('小贝识别成功:{}'.format(msg))
    control_ins = CommandController()
    control_ins.m_control(msg)
    return True


if __name__ == '__main__':
    count = 0
    # 程序运行10次，次数可修改
    while count < 10:
        m_res = motion_control_by_voice_sample()
        while not m_res:
            print('------------------------------------')
            print('未识别到正确指令，继续识别')
            m_res = motion_control_by_voice_sample()
        count += 1
