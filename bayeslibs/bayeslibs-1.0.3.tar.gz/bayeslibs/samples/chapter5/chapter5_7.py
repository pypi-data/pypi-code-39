# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/7/10
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from bayeslibs.voice import open_wakeup, start_speak, get_speak_status
from bayeslibs.voice import get_wakeup_status, open_asr, get_asr_status

LITERARY_STORY_LIST = ['高山流水', '庄周梦蝶', '炎黄子孙', '秦晋之好',
                       '纸上谈兵', '咏絮才高', '白云苍狗', '庖丁解牛']
LITERARY = 'LITERARY-ALLUSION'


def auto_speech_recognize():
    """
    APOLLO机器人语音识别
    """
    res_asr = open_asr()
    if res_asr and res_asr['status'] == 0:
        print('>>> 小贝语音识别功能打开成功 <<<')
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
        print('>>> 小贝唤醒识别功能打开成功 <<<')
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


def voice_play(text):
    """
       输入任意内容，让APOLLO机器人将其播放出来，实现语音合成功能
    """
    print(text)
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


def literary_story_sample():
    """
    进行语音交互：唤醒 “小贝”，让其播放自己讲解的文学典故
    目前支持的典故有：高山流水, 庄周梦蝶, 炎黄子孙, 秦晋之好,
                   纸上谈兵, 咏絮才高, 白云苍狗, 庖丁解牛
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
    for music_name in LITERARY_STORY_LIST:
        # 判断支持的文学典故是否在识别的文字里
        if music_name in text_reg:
            # 讲解文学典故，直至文学典故讲解完毕
            voice_play(LITERARY + music_name)
            return True
    return False


if __name__ == '__main__':
    m_res = literary_story_sample()
    while not m_res:
        print('文学典故讲解失败，继续识别')
        m_res = literary_story_sample()
    print('文学典故讲解成功，退出程序')
