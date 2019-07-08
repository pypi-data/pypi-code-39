# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.voice import start_speak, get_speak_status


def voice_play_sample(text):
    """
       输入任意内容，让APOLLO机器人将其播放出来，实现语音合成功能
    """
    start_res = start_speak(text)
    if start_res and start_res['status'] == 0:
        print('>>> 小贝语音合成功能打开成功 <<<')
        res = get_speak_status()
        while res['status'] == 0:
            print('------------------------------------')
            res = get_speak_status()
            print('小贝语音合成中.......')
        print('------------------------------------')
        print('小贝语音合成结束，退出程序')
        print('------------------------------------')
        return True
    else:
        return False


if __name__ == '__main__':
    count_ = 0
    # 程序运行10次，次数可修改
    while count_ < 10:
        question_ = input('请输入您要合成的语句:')
        print('------------------------------------')
        voice_play_sample(question_)
        count_ += 1
