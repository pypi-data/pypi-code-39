# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import face_register
from bayeslibs.vision import open_headpose_recognizer, close_headpose_recognizer
from bayeslibs.vision import get_headpose_recognized
from bayeslibs.vision import open_emotion_recognizer, close_emotion_recognizer
from bayeslibs.vision import get_emotions_recognized

HEADPOSE_YAW_ANGLE = 30  # 人脸左右旋转阈值
HEADPOSE_PITCH_ANGLE = 40  # 人脸上下俯仰阈值
HEADPOSE_ROLL_ANGLE = 10  # 人脸平面旋转阈值
# 可识别的表情
EMOTION_MAP = {
    'anger': '愤怒', 'disgust': '厌恶', 'fear': '恐惧', 'happy': '高兴',
    'sad': '伤心', 'supprise': '惊讶', 'neutual': '无情绪'
}
RUN_TIME = 30


class ApolloStudentMonitor:
    def __init__(self):
        pass

    @staticmethod
    def voice_notice(text):
        """
           输入提示信息，让APOLLO机器人将其播放出来
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
    def face_register(face_path):
        """
            人脸注册程序
            face_path:人脸库路径
        """
        print('人脸注册开始......')
        res = face_register(face_path=face_path)
        if res is True:
            print('人脸注册成功!')
        else:
            print('人脸注册失败!')
        return res

    def monitor(self, file_path):
        try:
            r_res = self.face_register(file_path)
            if not r_res:
                print('人脸库录入失败，请重新录入')
                return False
            h_res = open_headpose_recognizer()
            e_res = open_emotion_recognizer(False)
            if h_res['status'] == 0 and e_res['status'] == 0:
                print('>>> 学生认真程度检查功能打开成功 <<<')
                start_time = datetime.datetime.now()
                cur_time = datetime.datetime.now()
                while (cur_time - start_time).seconds < RUN_TIME:
                    # 获取头部姿态和表情数据，数据格式参考get_headpose_recognized函数说明
                    headposes = get_headpose_recognized()
                    emotions = get_emotions_recognized()
                    # status=0表示正确检测到头部姿态，条件判断通过后进行头部姿态数据解析
                    if headposes['status'] == 0:
                        for headpose in headposes['data']:
                            yaw_flag = abs(headpose['yaw']) > HEADPOSE_YAW_ANGLE
                            pitch_flag = abs(headpose['pitch']) > HEADPOSE_PITCH_ANGLE
                            roll_flag = abs(headpose['roll']) > HEADPOSE_ROLL_ANGLE
                            if yaw_flag or pitch_flag or roll_flag:
                                self.voice_notice('同学，你的姿态不太对哦，请调整一下')
                    if emotions['status'] == 0:
                        for emotion in emotions['data']:
                            print('-----------------------')
                            print('人脸表情类别:', EMOTION_MAP[emotion['emotion']])
                    cur_time = datetime.datetime.now()
                print('-----------------------')
                print('{}s运行时间已到，退出程序'.format(RUN_TIME))
                close_headpose_recognizer()
                close_emotion_recognizer()
                return True
            else:
                return False
        except Exception as err:
            print('ApolloStudentMonitor error:{}'.format(err))
            return False


if __name__ == '__main__':
    print('>>> 输入路径不能有中文 <<<')
    face_path_ = input('请输入人脸库所在路径:')
    apollo_cruise = ApolloStudentMonitor()
    apollo_cruise.monitor(face_path_)
