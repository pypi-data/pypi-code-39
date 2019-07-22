# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/7/11
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import close_face_detector, open_single_color_recognizer
from bayeslibs.vision import get_colors_recognized, close_color_recognizer
from abc import abstractmethod
from bayeslibs.motion import robot_move_forward, get_robot_move_status
from bayeslibs.motion import robot_move_back, get_robot_rotate_status
from bayeslibs.motion import robot_rotate_right, robot_rotate_left
import traceback

COLOR_MAP = {'red': '红色', 'blue': '蓝色', 'green': '绿色', 'yellow': '黄色'}
# 程序运行时间
RUN_TIME = 60
# 色块距离阈值
COLOR_DISTANCE_THR = 0.2
IMAGE_CENTER_X = 320


class ApolloMoveBase:
    def __init__(self):
        pass

    @staticmethod
    def get_move_status():
        try:
            print('------------------------------------')
            print('运动中.....')
            rotate_stat = get_robot_move_status()
            while rotate_stat['status'] != 0:
                rotate_stat = get_robot_move_status()
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


class ApolloColorTracker:
    """
       利用单一色卡教具，观察APOLLO如何实现单一颜色识别并检测色块的距离，
       不断调整与色块的距离，保证时刻追踪色块
    """

    def __init__(self):
        self.move_forward = ApolloMoveForward()
        self.rotate_right = ApolloRotateRight()
        self.rotate_left = ApolloRotateLeft()
        self.guest_gender = None

    @staticmethod
    def dist_detect(face_pos):
        """
           利用APOLLO机器人，检测特定图像的矩形框到深度摄像头之间的距离
        """
        from bayeslibs.vision import open_distance_detector, close_distance_detector
        from bayeslibs.vision import get_distance_detected
        pos = {
            'left': int(face_pos['left']),
            'top': int(face_pos['top']),
            'width': int(face_pos['width']),
            'height': int(face_pos['height'])
        }
        open_res = open_distance_detector(pos, False)  # 打开距离检测功能
        if open_res['status'] == 0:
            print('>>> 距离检测功能打开成功 <<<')
            count = 0
            # 如果检测到对应位置的距离信息则退出程序，否则循环5次后退出
            while count < 5:
                # 获取距离检测数据，数据格式参考get_distance_detected函数说明
                dist_detected = get_distance_detected()
                # status=0表示正确检测到距离，条件判断通过后进行距离数据解析
                if dist_detected['status'] == 0:
                    print('-----------------------')
                    dist = dist_detected['data']['dist']
                    print('distance: {}m'.format(dist_detected['data']['dist']))
                    close_distance_detector()
                    return dist
                count += 1
            print('-----------------------')
            print('>>> 距离检测结束 <<<')
            print('-----------------------')
            close_distance_detector()
            return None
        else:
            return None

    def track(self):
        try:
            color = input('请输入你要识别的颜色：')
            while color not in COLOR_MAP.keys():
                color = input('颜色输入错误，请重新输入你要识别的颜色：')
            color = color.strip()  # 消除字符串两边的空格
            open_res = open_single_color_recognizer(color)  # 打开颜色检测功能
            if open_res and open_res['status'] == 0:
                start_time = datetime.datetime.now()
                cur_time = datetime.datetime.now()
                print('-----------------------')
                print('{}色卡教具识别中...........'.format(COLOR_MAP[color]))
                print('-----------------------')
                while (cur_time - start_time).seconds < RUN_TIME:
                    # 获取颜色检测数据，数据格式参考get_color_recognized函数说明
                    color_recognized = get_colors_recognized()
                    # status=0表示正确检测到颜色，条件判断通过后进行颜色数据解析
                    if color_recognized and color_recognized['status'] == 0:
                        color_info = color_recognized['data'][0]
                        print('{}色卡教具已被识别'.format(COLOR_MAP[color]))
                        center_x = color_info['left'] + color_info['width'] / 2
                        dif_x = center_x - IMAGE_CENTER_X
                        print('色块中心点距离：{}'.format(dif_x))
                        if dif_x < 0 and abs(dif_x) > 30:
                            self.rotate_left.rotate(10)
                            print('-----------------------')
                            print('左转')
                            continue
                        if dif_x > 0 and abs(dif_x) > 30:
                            self.rotate_right.rotate(20)
                            print('-----------------------')
                            print('右转')
                            continue
                        dist = self.dist_detect(color_info)
                        if dist is None:
                            continue
                        print('dist:{}'.format(dist))
                        if 0 < dist < COLOR_DISTANCE_THR:
                            continue
                        elif dist > COLOR_DISTANCE_THR:
                            close_face_detector()
                            print('小贝向前运动')
                            print('-----------------------')
                            self.move_forward.move(2)
                            print('{}色卡教具识别中...........'.format(COLOR_MAP[color]))
                            print('-----------------------')
                    cur_time = datetime.datetime.now()
                print('------------------------------------')
                print('{}s运行时间已到，退出程序'.format(RUN_TIME))
                close_color_recognizer()
                return True
            else:
                return False
        except Exception as err:
            print('ApolloColorTracker error:{}\n{}'.format(err, traceback.print_exc()))
            return False


if __name__ == '__main__':
    apollo_cruise = ApolloColorTracker()
    apollo_cruise.track()
