# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.vision import open_beauty_age_gender_recognizer
from bayeslibs.vision import get_beauty_age_genders_recognized
from bayeslibs.vision import close_beauty_age_gender_recognizer

# 程序运行时间
RUN_TIME = 10


def beauty_age_gender_recog_sample():
    """
       判断某个人的性别以及实际年龄，并进行颜值打分
    """
    open_res = open_beauty_age_gender_recognizer()  # 打开颜值年龄性别识别功能
    if open_res['status'] == 0:
        print('>>> 颜值、年龄和性别识别功能打开成功 <<<')
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        while (cur_time - start_time).seconds < RUN_TIME:
            # 获取颜值年龄性别识别数据，数据格式参考get_beauty_age_genders_recognized函数说明
            beauty_recognized = get_beauty_age_genders_recognized()
            print('-----------------------')
            # status=0表示正确识别到颜值年龄性别，条件判断通过后进行颜值年龄性别数据解析
            if beauty_recognized['status'] == 0:
                print('识别成功，人脸数目：{}'.format(len(beauty_recognized['data'])))
                for beauty in beauty_recognized['data']:
                    print('性别:', beauty['gender'], end=', ')
                    print('年龄:', beauty['age'], end=', ')
                    print('颜值:', beauty['beauty'])
            else:
                print('没有识别到人脸信息，请调整至合适位置')
            cur_time = datetime.datetime.now()
        print('-----------------------')
        print('{}s运行时间已到，退出程序'.format(RUN_TIME))
        close_beauty_age_gender_recognizer()
        return True
    else:
        print(open_res)
        return False


if __name__ == '__main__':
    beauty_age_gender_recog_sample()
