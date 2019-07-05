# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import time
from bayeslibs.voice import open_wakeup, get_wakeup_status, close_wakeup


def wakeup_sample(res_word):
    """
    呼唤“小贝、小贝”，观察 APOLLO小车的唤醒情况
    """
    open_res = open_wakeup(res_word)
    if open_res and open_res['status'] == 0:
        print('>>> 小贝唤醒识别功能打开成功 <<<')
        res = get_wakeup_status()
        while res['status'] != 0:
            print('------------------------------------')
            res = get_wakeup_status()
            print('小贝等待唤醒中.......')
        print('------------------------------------')
        print('小贝唤醒成功，唤醒角度:{}'.format(res['angle']))
        print('------------------------------------')
        print('语音播放中.......')
        print('------------------------------------')
        # 暂停播放答复词，暂停时长随答复词长短而定
        time.sleep(2)
        close_wakeup()
        print('运行结束，退出程序')
        return True
    else:
        return False


if __name__ == '__main__':
    res_word_ = input('请输入唤醒小贝后的答复词:')
    wakeup_sample(res_word_)
