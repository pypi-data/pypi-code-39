# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.motion import start_auto_nav, get_auto_nav_status, stop_auto_nav
from bayeslibs.vision import open_face_detector, close_face_detector, get_faces_detected
from bayeslibs.vision import open_face_recognizer, close_face_recognizer, get_faces_recognized
from bayeslibs.vision import open_handpose_recognizer, close_handpose_recognizer
from bayeslibs.vision import get_handposes_recognized
from samples.config import get_slam_map, add_slam_pos
import time

FOOD_ROOM = 'p_food'
DINING_TABLE = 'p_12table'
ORIGIN_PLACE = 'p_origin'
DESTINATION_POS_MAP = {'p_food': {'x': 6.040, 'y': 6.404},
                       'p_12table': {'x': -1.131, 'y': -4.171}, 'p_origin': {'x': 0, 'y': 0}}
NAV_TIME = 60 * 20

FACE_DETECT_TIME = 30
FACE_PROBABILITY = 0.9
HANDPOSE_LIST = ['One', 'Two', 'Ok']

HANDPOSE_RUN_TIME = 30
HANDPOSE_LOOP = 2

FACE_RECOG_TIME = 30
VIP_MAP = {'chenwei': '陈伟', 'shuqing': '舒庆', 'qianyang': '钱扬', 'yewei': '叶伟'}


def update_nav_pos():
    """
    更新室内导航地图位置信息
    :return: True
    """
    for item, pos in DESTINATION_POS_MAP.items():
        add_slam_pos(item, pos['x'], pos['y'])
    return True


class ApolloAGV:
    def __init__(self):
        self.handpose = list()

    @staticmethod
    def voice_notice(text):
        """
           输入提示信息，让APOLLO机器人将其播放出来
        """
        from bayeslibs.voice import start_speak, get_speak_status
        start_res = start_speak(text)
        if start_res and start_res['status'] == 0:
            print('>>> 小贝语音合成功能打开成功 <<<')
            s_res = get_speak_status()
            print('------------------------------------')
            print('小贝语音合成中.......')
            while s_res['status'] == 0:
                s_res = get_speak_status()
            time.sleep(0.2)
            print('------------------------------------')
            print('>>> 小贝语音合成结束 <<<')
            print('------------------------------------')
            return True
        else:
            return False

    def handpose_recog(self):
        """
           捕捉摄像头前的OK手势
        """
        open_res = open_handpose_recognizer()  # 打开年龄性别检测功能
        if open_res['status'] == 0:
            print('>>> 手势识别功能打开成功 <<<')
            start_time = datetime.datetime.now()
            cur_time = datetime.datetime.now()
            while (cur_time - start_time).seconds < HANDPOSE_RUN_TIME:
                # 获取手势识别数据，数据格式参考get_handposes_recognized函数说明
                handpose_recognized = get_handposes_recognized()
                # status=0表示正确检测到手势，条件判断通过后进行手势数据解析
                if handpose_recognized['status'] == 0:
                    print('手势识别成功，手势识别数目：{}'.format(len(handpose_recognized['data'])))
                    for handpose in handpose_recognized['data']:
                        if handpose['classname'] not in HANDPOSE_LIST:
                            print('-----------------------')
                            print('手势不对，请调整至OK')
                            continue
                        if len(self.handpose) == 0 and handpose['classname'] == 'Ok':
                            print('-----------------------')
                            print('手势OK识别正确')
                            self.handpose.append('OK')
                            print('-----------------------')
                            self.voice_notice('菜品已经成功放置，谢谢')
                            close_handpose_recognizer()
                            return True
                cur_time = datetime.datetime.now()
            print('-----------------------')
            print('{}s运行时间已到，退出程序'.format(HANDPOSE_RUN_TIME))
            close_handpose_recognizer()
            return False
        else:
            return False

    def face_detect(self):
        """
           多人人脸检测
        """
        open_res = open_face_detector()  # 打开人脸检测功能
        if open_res['status'] == 0:
            print('>>> 人脸检测功能打开成功 <<<')
            start_time = datetime.datetime.now()
            cur_time = datetime.datetime.now()
            while (cur_time - start_time).seconds < FACE_DETECT_TIME:
                # 获取人脸检测数据，数据格式参考get_faces_detected函数说明
                faces_detected = get_faces_detected()
                print('-----------------------')
                # status=0表示正确检测到人脸，条件判断通过后进行人脸数据解析
                if faces_detected['status'] == 0:
                    print('人脸检测成功，人脸数目：{}'.format(len(faces_detected['data'])))
                    for face in faces_detected['data']:
                        print('目标名称:', face['object_name'], end=', ')
                        print('人脸概率:', face['probability'])
                        if face['probability'] > FACE_PROBABILITY:
                            self.voice_notice('您好，请将12号桌的菜品放到面板上，菜品放置完毕后， 请做OK的手势')
                            close_face_detector()
                            return True
                else:
                    print('没有检测到人脸信息，请调整至合适位置')
                cur_time = datetime.datetime.now()
            print('-----------------------')
            print('{}s运行时间已到，退出程序'.format(FACE_DETECT_TIME))
            close_face_detector()
            return False
        else:
            return False

    def vip_recog_notice(self):
        """
           人脸识别
        """
        open_res = open_face_recognizer()  # 打开人脸识别功能
        if open_res['status'] == 0:
            print('>>> 多人人脸识别功能打开成功 <<<')
            start_time = datetime.datetime.now()
            cur_time = datetime.datetime.now()
            while (cur_time - start_time).seconds < FACE_RECOG_TIME:
                # 获取人脸识别数据，数据格式参考get_faces_recognized函数说明
                faces_recognized = get_faces_recognized()
                print('-----------------------')
                # status=0表示正确检测到人脸，条件判断通过后进行人脸数据解析
                if faces_recognized['status'] == 0:
                    print('人脸识别成功，人脸数目：{}'.format(len(faces_recognized['data'])))
                    for face in faces_recognized['data']:
                        print('人脸名称:', face['face_name'], end=', ')
                        print('人脸得分:', face['score'])
                        if face['face_name'] in VIP_MAP.keys():
                            self.voice_notice('{}，请取走您的餐品'.format(VIP_MAP[face['face_name']]))
                            close_face_recognizer()
                            return True
                else:
                    print('没有识别到VIP信息，请调整至合适位置')
                cur_time = datetime.datetime.now()
            print('-----------------------')
            print('{}s运行时间已到，退出程序'.format(FACE_RECOG_TIME))
            close_face_recognizer()
            return False
        else:
            return False

    def get_medicine(self):
        try:
            f_res = self.face_detect()
            if not f_res:
                self.voice_notice('您好，请将12号桌的菜品放到面板上，菜品放置完毕后， 请做OK的手势')
            count = 1
            time.sleep(2)
            self.voice_notice('您好，请您做OK的手势')
            h_res = self.handpose_recog()
            self.handpose = list()
            while not h_res:
                if count > HANDPOSE_LOOP:
                    return False
                self.voice_notice('手势无法正确识别，请重新做OK的手势')
                print('------------------------------------')
                print('重新进行手势识别')
                count += 1
                h_res = self.handpose_recog()
            return True
        except Exception as err:
            print('ApolloAGV get_medicine error:{}'.format(err))
            return False

    @staticmethod
    def auto_guided_position(dest):
        if dest not in get_slam_map():
            print('地点输入有误，请重新配置导航地点')
            return False
        stat_res = start_auto_nav(dest)
        if stat_res and stat_res['status'] == 0:
            print('>>> 小贝自动导航功能打开成功 <<<')
            start_time = datetime.datetime.now()
            cur_time = datetime.datetime.now()
            stat = get_auto_nav_status()
            print('------------------------------------')
            print('小贝导航中.......')
            # 60*20s如果还没有导航成功就取消导航
            while stat and stat['status'] != 0 and (cur_time - start_time).seconds <= NAV_TIME:
                stat = get_auto_nav_status()
                cur_time = datetime.datetime.now()
            if (cur_time - start_time).seconds > NAV_TIME:
                print('------------------------------------')
                print('小贝导航超时.......{}s运行时间已到，退出程序'.format(NAV_TIME))
                n_res = stop_auto_nav()
                if n_res['status'] == 0:
                    print('导航关闭成功')
                    return False
            print('------------------------------------')
            print('小贝导航成功.......')
            print('------------------------------------')
            return True
        else:
            print('网络故障，请检查网络状况是否良好')
            return False

    def back_home(self):
        o_nav_res = self.auto_guided_position(ORIGIN_PLACE)
        if not o_nav_res:
            print('------------------------------------')
            print('返回原点导航失败，请检查程序和小车配置，确认无误后重启程序')
            return False
        return True

    def auto_guided_vehicle(self):
        try:
            f_nav_res = self.auto_guided_position(FOOD_ROOM)
            if not f_nav_res:
                print('------------------------------------')
                print('取餐室导航失败，小车将返回原点')
                return self.back_home()
            md_res = self.get_medicine()
            if not md_res:
                print('------------------------------------')
                print('取药失败，小车将返回原点')
                return self.back_home()
            d_nav_res = self.auto_guided_position(DINING_TABLE)
            if not d_nav_res:
                print('------------------------------------')
                print('12号餐桌导航失败，小车将返回原点')
                return self.back_home()
            vip_res = self.vip_recog_notice()
            if not vip_res:
                print('------------------------------------')
                print('VIP用户无法识别，小车将返回原点')
            time.sleep(1)
            self.voice_notice('菜品已经成功送达，小贝要回去了，谢谢')
            return self.back_home()
        except Exception as err:
            print('ApolloAGV error:{}'.format(err))
            return False


if __name__ == '__main__':
    # 更新室内导航地图位置信息
    update_nav_pos()
    apollo_cruise = ApolloAGV()
    res = apollo_cruise.auto_guided_vehicle()
    if res:
        print('------------------------------------')
        print('程序运行成功')
    else:
        print('------------------------------------')
        print('程序异常退出')
