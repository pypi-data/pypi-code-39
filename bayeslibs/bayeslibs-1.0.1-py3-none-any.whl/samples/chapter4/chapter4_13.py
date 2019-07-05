# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_skeleton_recognizer, get_skeletons_recognized
from bayeslibs.vision import close_skeleton_recognizer

# 程序运行时间
RUN_TIME = 30


def skeleton_recog_sample():
    """
       对摄像头前所捕捉到的人体图像的骨骼进行回显
    """
    open_res = open_skeleton_recognizer()  # 打开年龄性别检测功能
    if open_res['status'] == 0:
        print('>>> 骨骼识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取骨骼识别数据，数据格式参考get_skeletons_recognized函数说明
            skeleton_recognized = get_skeletons_recognized()
            print('-----------------------')
            # status=0表示正确检测到骨骼，条件判断通过后进行骨骼数据解析
            if skeleton_recognized['status'] == 0:
                print('人体骨骼识别成功，人体数目：{}'.format(len(skeleton_recognized['data'])))
                for skeleton_info in skeleton_recognized['data']:
                    print('骨骼关键节点:', skeleton_info['body_parts'])
            else:
                print('没有识别到骨骼信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_skeleton_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    skeleton_recog_sample()
