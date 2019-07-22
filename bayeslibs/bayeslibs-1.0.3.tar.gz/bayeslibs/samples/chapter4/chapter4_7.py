# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_object_detector, get_objects_detected, close_object_detector

# 程序运行时间
RUN_TIME = 30


def multi_object_detect_sample():
    """
       多物体检测
    """
    open_res = open_object_detector()  # 打开物体检测功能
    if open_res['status'] == 0:
        print('>>> 多物体检测功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取物体检测数据，数据格式参考get_faces_detected函数说明
            objects_detected = get_objects_detected()
            print('-----------------------')
            # status=0表示正确检测到物体，条件判断通过后进行物体数据解析
            if objects_detected['status'] == 0:
                print('物体检测成功，物体数目：{}'.format(len(objects_detected['data'])))
                for object_info in objects_detected['data']:
                    print('物体名称:', object_info['object_name'], end=', ')
                    print('物体概率:', object_info['probability'])
            else:
                print('没有检测到物体信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_object_detector()
        return True
    else:
        return False


if __name__ == '__main__':
    '''
    Python以模块运行方式启动入口
    '''
    multi_object_detect_sample()
