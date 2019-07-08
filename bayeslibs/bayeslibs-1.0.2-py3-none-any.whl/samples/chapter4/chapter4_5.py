# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_face_detector, get_faces_detected, close_face_detector

# 程序运行时间
RUN_TIME = 10


def multi_face_detect_sample():
    """
       多人人脸检测
    """
    open_res = open_face_detector()  # 打开人脸检测功能
    if open_res['status'] == 0:
        print('>>> 多人人脸检测功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取人脸检测数据，数据格式参考get_faces_detected函数说明
            faces_detected = get_faces_detected()
            print('-----------------------')
            # status=0表示正确检测到人脸，条件判断通过后进行人脸数据解析
            if faces_detected['status'] == 0:
                print('人脸检测成功，人脸数目：{}'.format(len(faces_detected['data'])))
                for face in faces_detected['data']:
                    print('目标名称:', face['object_name'], end=', ')
                    print('人脸概率:', face['probability'])
            else:
                print('没有检测到人脸信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_face_detector()
        return True
    else:
        return False


if __name__ == '__main__':
    multi_face_detect_sample()
