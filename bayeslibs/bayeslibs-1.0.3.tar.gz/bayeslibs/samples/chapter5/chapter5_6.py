# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.voice import get_wakeup_status, open_asr, get_asr_status
from bayeslibs.voice import open_wakeup
from bayeslibs.voice import start_small_talk, start_speak, get_speak_status


def voice_play(text):
    """
       输入任意内容，让APOLLO机器人将其播放出来，实现语音合成功能
    """
    start_res = start_speak(text)
    if start_res and start_res['status'] == 0:
        res = get_speak_status()
        print('------------------------------------')
        print('小贝语音合成中.......')
        while res['status'] == 0:
            res = get_speak_status()
        return True
    else:
        return False


def apollo_chat(question):
    """
    语音输入自己想说的话，观察APOLLO的自然语言处理结果
    """
    result = start_small_talk(question)
    if result['status'] == 0:
        answer = result['answer']
        print('小贝的回答:{}'.format(answer))
    else:
        print('小贝还小，还有很多需要学习')
        answer = '小贝还小，还有很多需要学习'
    return answer


def auto_speech_recognize():
    """
    APOLLO机器人语音识别
    """
    res_asr = open_asr()
    if res_asr and res_asr['status'] == 0:
        stat = get_asr_status()
        print('------------------------------------')
        print('小贝识别中.......')
        while stat and stat['is_asr']:
            stat = get_asr_status()
        print('------------------------------------')
        if 'text' in stat and stat['text']:
            print('小贝识别成功:{}'.format(stat['text']))
            print('------------------------------------')
            res = stat['text']
            return True, res
        else:
            res = '不好意思，小贝没有听清你的声音'
            return False, res
    else:
        return False, '网络故障'


def wakeup():
    """
    唤醒小贝
    """
    open_res = open_wakeup()
    if open_res and open_res['status'] == 0:
        res = get_wakeup_status()
        print('------------------------------------')
        print('小贝等待唤醒中.......')
        while res['status'] != 0:
            res = get_wakeup_status()
        print('------------------------------------')
        print('小贝唤醒成功，唤醒角度:{}'.format(res['angle']))
        return True
    else:
        return False


def voice_chat_sample():
    """
    天气问询：唤醒 “小贝”，查询某一个城市（如常州）的实时天气，以及语音闲聊
    """
    # 首先进行语音唤醒
    w_res = wakeup()
    if not w_res:
        print('小贝唤醒失败，请监测网络设备')
        return False
    # 唤醒成功后进行语音识别
    ret, text_reg = auto_speech_recognize()
    if not ret:
        print('小贝识别失败，请重新唤醒和识别')
        return False
    answer = apollo_chat(text_reg)
    voice_play(answer)
    return True


if __name__ == '__main__':
    count_ = 0
    # 循环聊天10次，次数可修改
    while count_ < 10:
        voice_chat_sample()
        count_ += 1
