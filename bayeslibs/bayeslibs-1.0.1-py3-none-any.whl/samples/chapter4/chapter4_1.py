# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_single_color_recognizer, get_colors_recognized
from bayeslibs.vision import close_color_recognizer

COLOR_MAP = {'red': '红色', 'blue': '蓝色', 'green': '绿色', 'yellow': '黄色'}
# 程序运行时间
RUN_TIME = 10


def single_color_recog_sample():
    """
       利用单一色卡教具，观察APOLLO如何实现单一颜色识别并将返回的数据结果进行解析
       目前支持的颜色：red,blue,green,yellow
    """
    color = input('请输入你要识别的颜色：')
    while color not in COLOR_MAP.keys():
        color = input('颜色输入错误，请重新输入你要识别的颜色：')
    color = color.strip()  # 消除字符串两边的空格
    open_res = open_single_color_recognizer(color)  # 打开颜色检测功能
    if open_res and open_res['status'] == 0:
        print('>>> 单一色卡识别功能打开成功 <<<')
        print('*** 提示1：请将单一色卡教具放置在Apollo小车的RealSense摄像头可捕捉的范围内 ***')
        print('*** 提示2：程序运行时间可通过修改参数RUN_TIME实现，默认运行30s***')
        print('*** 提示3：如果程序结果提示计算机积极拒绝，说明没有配置Apollo网络，请先配置网络***')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取颜色检测数据，数据格式参考get_color_recognized函数说明
            color_recognized = get_colors_recognized()
            print('------------------------------------')
            # status=0表示正确检测到颜色，条件判断通过后进行颜色数据解析
            if color_recognized and color_recognized['status'] == 0:
                color_info = color_recognized['data'][0]
                # round()将浮点数进行四舍五入变成整型数据
                print('{}色卡教具已被识别，色卡面积为{}像素'.format(COLOR_MAP[color],
                                                    round(color_info['area'])))
            else:
                print('没有识别到{}色卡教具，请调整至合适位置'.format(COLOR_MAP[color]))
            cur_time = datetime.datetime.now()
        print('------------------------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_color_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    single_color_recog_sample()
