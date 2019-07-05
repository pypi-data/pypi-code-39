# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_multi_color_recognizer, get_colors_recognized
from bayeslibs.vision import close_color_recognizer

COLOR_MAP = {'red': '红色', 'blue': '蓝色', 'green': '绿色', 'yellow': '黄色'}
# 程序运行时间
RUN_TIME = 30


def multi_color_recog_sample():
    """
       利用多颜色色卡教具，让APOLLO同时实现多种颜色的识别，并把识别出的颜色按照面积大小进行排序
       目前支持的颜色：red,blue,green,yellow
    """
    # 颜色输入中间以英文,隔开: red,blue
    colors = input('请输入你要识别的颜色：')
    input_check = False
    while not input_check:
        for color in colors.split(','):
            color = color.strip()  # 消除字符串两边的空格
            input_check = False if color not in COLOR_MAP.keys() else True
        if input_check:
            break
        colors = input('颜色输入错误，请重新输入你要识别的颜色：')
    open_res = open_multi_color_recognizer(colors)  # 打开多颜色识别功能
    if open_res and open_res['status'] == 0:
        print('>>> 多颜色色卡识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取颜色检测数据，数据格式参考get_color_recognized函数说明
            colors_recognized = get_colors_recognized()
            # status=0表示正确检测到颜色，条件判断通过后进行颜色数据解析,并按照面积大小进行排序
            if colors_recognized and colors_recognized['status'] == 0:
                colors_info = colors_recognized['data']
                # 按照面积大小对颜色数据进行排序
                colors_info = sorted(colors_info, key=lambda item: item['area'], reverse=True)
                print('---------------------------------------------')
                for ind, color_info in enumerate(colors_info):
                    # round()将浮点数进行四舍五入变成整型数据
                    print('面积大小顺序：{}，{}色块已被识别，色卡面积为：{}'.format(
                        ind + 1, COLOR_MAP[color_info['color']], round(color_info['area'])))
            else:
                print('没有识别到多颜色色卡教具，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('---------------------------------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_color_recognizer()
        return True
    else:
        return False


if __name__ == '__main__':
    multi_color_recog_sample()
