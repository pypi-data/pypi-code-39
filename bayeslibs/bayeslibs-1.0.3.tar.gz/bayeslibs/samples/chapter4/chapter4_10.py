# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_headpose_recognizer, get_headpose_recognized
from bayeslibs.vision import close_headpose_recognizer

# 程序运行时间
RUN_TIME = 30


def headpose_recog_sample():
    """
       判断班级某一个人当时的头部姿态
    """
    # 打开头部姿态检测功能
    open_res = open_headpose_recognizer()
    if open_res['status'] == 0:
        print('>>> 头部姿态识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取头部姿态检测数据，数据格式参考get_headpose_recognized函数说明
            headposes_detected = get_headpose_recognized()
            print('-----------------------')
            # status=0表示正确检测到头部姿态，条件判断通过后进行头部姿态数据解析
            if headposes_detected['status'] == 0:
                for ind, headpose in enumerate(headposes_detected['data']):
                    print('人脸序号：{}'.format(ind))
                    print('三维旋转之左右旋转角[-90(左), 90(右)]:', headpose['yaw'])
                    print('三维旋转之俯仰角度[-90(上), 90(下)]:', headpose['pitch'])
                    print('平面内旋转角[-180(逆时针), 180(顺时针)]:', headpose['roll'])
            else:
                print('没有识别到头部姿态信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_headpose_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    headpose_recog_sample()
