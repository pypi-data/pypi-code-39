# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_emotion_recognizer, get_emotions_recognized
from bayeslibs.vision import close_emotion_recognizer

# 程序运行时间
RUN_TIME = 10

# 可识别的表情
EMOTION_MAP = {
    'anger': '愤怒', 'disgust': '厌恶', 'fear': '恐惧', 'happy': '高兴',
    'sad': '伤心', 'supprise': '惊讶', 'neutual': '无情绪'
}


def multi_face_emotion_recog_sample():
    """
        多人人脸表情识别
    """
    open_res = open_emotion_recognizer()  # 打开表情识别功能
    if open_res['status'] == 0:
        print('>>> 多人人脸表情识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取表情识别数据，数据格式参考get_emotions_recognized函数说明
            emotions_detected = get_emotions_recognized()
            print('-----------------------')
            # status=0表示正确检测到表情，条件判断通过后进行表情识别数据解析
            if emotions_detected['status'] == 0:
                print('人脸表情识别成功，人脸表情数目：{}'.format(len(emotions_detected['data'])))
                for emotion in emotions_detected['data']:
                    print('人脸表情类别:', EMOTION_MAP[emotion['emotion']])
            else:
                print('没有识别到人脸表情信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_emotion_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    multi_face_emotion_recog_sample()
