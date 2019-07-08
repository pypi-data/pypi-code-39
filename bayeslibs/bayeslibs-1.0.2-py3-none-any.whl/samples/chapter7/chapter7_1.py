# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_face_detector, close_face_detector, get_faces_detected
from bayeslibs.vision import close_beauty_age_gender_recognizer
from bayeslibs.vision import get_beauty_age_genders_recognized
from bayeslibs.vision import open_beauty_age_gender_recognizer
from abc import abstractmethod
from bayeslibs.motion import robot_move_forward, get_robot_move_status, robot_move_back
import traceback
from math import pi, cos

FACE_DETECT_FACE_PROB = 0.90  # 人脸检测的概率
FACE_DISTANCE_THR = 0.5  # 人脸距离阈值

# 程序运行时间
RUN_TIME = 60
# 摄像头上斜角度
CAMERA_ANGLE = 60 * pi / 180


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


class ApolloGreeter:
    __GENDER_MAP = {'male': '先生', 'female': '女士', 'Male': '先生', 'Female': '女士'}

    def __init__(self):
        self.move_forward = ApolloMoveForward()
        self.guest_gender = None

    @staticmethod
    def product_introduce(text):
        """
           输入产品讲解信息，让APOLLO机器人将其播放出来
        """
        from bayeslibs.voice import start_speak, get_speak_status
        start_res = start_speak(text)
        if start_res and start_res['status'] == 0:
            print('>>> 小贝语音合成功能打开成功 <<<')
            res = get_speak_status()
            print('------------------------------------')
            print('小贝语音合成中.......')
            while res['status'] == 0:
                res = get_speak_status()
            print('------------------------------------')
            print('>>> 小贝语音合成结束 <<<')
            print('------------------------------------')
            return True
        else:
            return False

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

    @staticmethod
    def person_gender_recog(face_pos):
        """
           判断特定矩形框中人的性别
        """
        if face_pos is None:
            return None
        # 打开性别识别功能
        open_res = open_beauty_age_gender_recognizer()
        if open_res['status'] == 0:
            print('>>>性别识别功能打开成功 <<<')
            count = 0
            # 如果检测到对应位置的性别信息则退出程序，否则循环100次后退出
            while count < 500:
                # 获取性别识别数据，数据格式参考get_beauty_age_genders_recognized函数说明
                gender_recognized = get_beauty_age_genders_recognized()

                # status=0表示正确识别到性别，条件判断通过后进行性别数据解析
                if gender_recognized['status'] == 0:
                    print('识别成功，人脸数目：{}'.format(len(gender_recognized['data'])))
                    for gender in gender_recognized['data']:
                        pos_left_diff = abs(gender['left'] - face_pos['left']) < 50
                        pos_top_diff = abs(gender['top'] - face_pos['top']) < 50
                        pos_width_diff = abs(gender['width'] - face_pos['width']) < 50
                        pos_height_diff = abs(gender['height'] - face_pos['height']) < 50
                        if pos_left_diff and pos_top_diff and pos_width_diff and pos_height_diff:
                            print('-----------------------')
                            print('性别:', gender['gender'], end=', ')
                            print('年龄:', gender['age'], end=', ')
                            print('颜值:', gender['beauty'])
                            close_beauty_age_gender_recognizer()
                            print('-----------------------')
                            return gender['gender']
                count += 1
            close_beauty_age_gender_recognizer()
            return None
        else:
            return None

    def greet_run(self):
        try:
            open_res = open_face_detector()  # 打开人脸检测功能
            if open_res['status'] == 0:
                print('>>> 机器人迎宾功能打开成功 <<<')
                start_time = datetime.datetime.now()
                cur_time = datetime.datetime.now()
                while (cur_time - start_time).seconds < RUN_TIME:
                    # 获取人脸检测数据，数据格式参考get_faces_detected函数说明
                    faces = get_faces_detected()
                    # status=0表示正确检测到人脸，条件判断通过后进行人脸数据解析
                    if faces['status'] == 0:
                        print('人脸检测成功，人脸数目：{}'.format(len(faces['data'])))
                        dist = 100
                        ind = 0
                        for index, face in enumerate(faces['data']):
                            print('目标名称:', face['object_name'], end=', ')
                            print('人脸概率:', face['probability'])
                            dist_tmp = self.dist_detect(face)
                            if dist_tmp and dist_tmp < dist:
                                dist = dist_tmp
                                ind = index
                        if faces['data'][ind]['probability'] < FACE_DETECT_FACE_PROB:
                            continue
                        if dist == 100:
                            continue
                        if 0 < dist < FACE_DISTANCE_THR:
                            continue
                        elif dist > FACE_DISTANCE_THR:
                            close_face_detector()
                            self.guest_gender = self.person_gender_recog(faces['data'][ind])
                            print('dist:{}'.format(dist))
                            print('小贝向前运动')
                            print('-----------------------')
                            self.move_forward.move(4)
                            break
                    cur_time = datetime.datetime.now()
                print('-----------------------')
                if self.guest_gender is None:
                    self.product_introduce('贵宾，您好。请让我为您讲解我公司的产品信息')
                else:
                    self.product_introduce('{}，您好。请让我为您讲解我公司的产品信息'.format(
                        self.__GENDER_MAP[self.guest_gender]))
                self.product_introduce('APOLLO小车是贝叶斯智能自主研发、面向AI教学的机器人平台。硬件包含'
                                       '激光雷达、深度摄像头、运动底盘等核心设备。依托此平台，同学们能就定'
                                       '位导航、物体检测、人脸识别、语音交互等主流AI应用进行实践学习。')
                print('-----------------------')
                print('程序运行完成，退出程序')
                close_face_detector()
                return True
            else:
                return False
        except Exception as err:
            print('ApolloGreeter error:{}\n{}'.format(err, traceback.print_exc()))
            return False


if __name__ == '__main__':
    apollo_cruise = ApolloGreeter()
    apollo_cruise.greet_run()
