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
import numpy as np

# 程序运行时间
RUN_TIME = 10


def file_path_validate(file_path):
    try:
        with open(file_path, 'a', encoding='utf-8') as f:
            f.write(str('depth data header\n'))
        return True
    except Exception as err:
        print('file save failed:{}'.format(err))
        return False


def depth_img_show_sample(file_path):
    """
       利用APOLLO机器人，捕捉摄像头前的图像，对图像的深度信息进行二维矩阵显示，并保存其深度文件
    """
    while not file_path_validate(file_path):
        file_path = input('路径输入有误，请重新输入:')
    # 限定深度图像获取范围
    pos = {
        'left': 270,
        'top': 190,
        'width': 10,
        'height': 10
    }
    # 打开距离检测功能
    open_res = open_distance_detector(pos)
    if open_res['status'] == 0:
        print('>>> 深度信息识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        # 判断深度数据是否保存，防止文件过大
        save_flag = False
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取深度信息数据，数据格式参考get_distance_detected函数说明
            dist_detected = get_distance_detected()
            print('-----------------------------------------------------')
            # status=0表示正确检测到距离，条件判断通过后进行距离数据解析
            if dist_detected['status'] == 0:
                dist_data = np.array(dist_detected['data']['dist_data']).reshape(
                    pos['width'], pos['height'])
                print('depth data\n{}'.format(dist_data))
                if not save_flag:
                    with open(file_path, 'a', encoding='utf-8') as f:
                        f.write('{}\n'.format(str(dist_data.tolist())))
                        save_flag = True
            else:
                print('没有识别到深度信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------------------------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_distance_detector()
        return True
    else:
        return False


if __name__ == '__main__':
    '''
    Python以模块运行方式启动入口
    '''
    depth_save_path = input('请输入深度数据保存路径:')
    depth_img_show_sample(depth_save_path)
