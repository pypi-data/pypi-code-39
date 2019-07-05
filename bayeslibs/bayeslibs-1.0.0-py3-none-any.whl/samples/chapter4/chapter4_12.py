# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_handpose_recognizer, get_handposes_recognized
from bayeslibs.vision import close_handpose_recognizer

HANDPOSE_MAP = {'Fist': '石头', 'Two': '剪刀', 'Five': '布', 'Ok': 'OK'}
# 程序运行时间
RUN_TIME = 30


def handpose_recog_sample():
    """
       对摄像头前所捕捉到的手势（OK、剪刀、石头、布等）进行回显
    """
    open_res = open_handpose_recognizer()  # 打开年龄性别检测功能
    if open_res['status'] == 0:
        print('>>> 手势识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取手势识别数据，数据格式参考get_handposes_recognized函数说明
            handpose_recognized = get_handposes_recognized()
            print('-----------------------')
            # status=0表示正确识别到手势，条件判断通过后进行手势数据解析
            if handpose_recognized['status'] == 0:
                print('手势识别成功，手势识别数目：{}'.format(len(handpose_recognized['data'])))
                for handpose in handpose_recognized['data']:
                    classname = handpose['classname']
                    if classname == 'Face':
                        continue
                    elif classname not in HANDPOSE_MAP:
                        print('手势不对，请调整至石头剪刀布或者OK')
                        continue
                    else:
                        classname = HANDPOSE_MAP[classname]
                        print('手势名称:', classname, end=', ')
                        print('手势概率:', handpose['probability'])
            else:
                print('没有识别到手势信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_handpose_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    handpose_recog_sample()
