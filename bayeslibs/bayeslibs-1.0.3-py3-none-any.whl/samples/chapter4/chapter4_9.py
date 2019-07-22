# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_face_recognizer, get_faces_recognized, close_face_recognizer

# 程序运行时间
RUN_TIME = 30


def multi_face_recog_sample():
    """
       多人人脸识别
    """
    open_res = open_face_recognizer()  # 打开人脸识别功能
    if open_res['status'] == 0:
        print('>>> 多人人脸识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取人脸识别数据，数据格式参考get_faces_recognized函数说明
            faces_recognized = get_faces_recognized()
            print('-----------------------')
            # status=0表示正确检测到人脸，条件判断通过后进行人脸数据解析
            if faces_recognized['status'] == 0:
                print('人脸识别成功，人脸数目：{}'.format(len(faces_recognized['data'])))
                for face in faces_recognized['data']:
                    print('人脸名称:', face['face_name'], end=', ')
                    print('人脸得分:', face['score'])
            else:
                print('没有识别到人脸信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_face_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    multi_face_recog_sample()
