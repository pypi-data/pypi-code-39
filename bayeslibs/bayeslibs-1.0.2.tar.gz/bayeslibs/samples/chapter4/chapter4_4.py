# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_distance_detector, get_distance_detected
from bayeslibs.vision import close_distance_detector

# 程序运行时间
RUN_TIME = 10


def center_point_distance_detect_sample():
    """
       利用APOLLO机器人，检测特定图像的中央点到深度摄像头之间的距离
    """
    # 限定深度图像获取范围
    pos = {
        'left': 270,
        'top': 190,
        'width': 50,
        'height': 50
    }
    open_res = open_distance_detector(pos)  # 打开距离检测功能
    if open_res['status'] == 0:
        print('>>> 图像中心点距离检测功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取距离检测数据，数据格式参考get_distance_detected函数说明
            dist_detected = get_distance_detected()
            print('-----------------------')
            # status=0表示正确检测到距离，条件判断通过后进行距离数据解析
            if dist_detected['status'] == 0:
                print('distance: {}m'.format(dist_detected['data']['dist']))
            else:
                print('没有检测到距离信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_distance_detector()
        return True
    else:
        return False


if __name__ == '__main__':
    '''
    Python以模块运行方式启动入口
    '''
    center_point_distance_detect_sample()
