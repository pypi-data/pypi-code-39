# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import time
from bayeslibs.voice import open_asr, get_asr_status, start_speak, close_asr


def auto_speech_recognize_sample():
    """
    APOLLO机器人语音识别
    """
    res_asr = open_asr()
    print(res_asr)
    if res_asr and res_asr['status'] == 0:
        print('>>> 小贝语音识别功能打开成功 <<<')
        stat = get_asr_status()
        print(stat)
        while stat and stat['is_asr']:
            print('------------------------------------')
            stat = get_asr_status()
            print('小贝识别中.......')
        print('------------------------------------')
        if 'text' in stat and stat['text']:
            print('小贝识别成功:{}'.format(stat['text']))
            start_speak(stat['text'])
            print('------------------------------------')
            time.sleep(2)
        else:
            print('小贝识别失败')
            print('------------------------------------')
            start_speak('不好意思，小贝没有听清你的声音')
            time.sleep(2)
        print('语音播放中.......')
        close_asr()
        print('------------------------------------')
        print('运行结束，退出程序')
        return True
    else:
        return False


if __name__ == '__main__':
    auto_speech_recognize_sample()
