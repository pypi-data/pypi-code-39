# conding=utf-8
"""
@project:edubalibs
@language:Python3
@create:2019/6/28
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
import datetime
from bayeslibs.voice import stop_music, start_music, get_music_status, open_wakeup
from bayeslibs.voice import get_wakeup_status, open_asr, get_asr_status

MUSIC_LIST = ['来自天堂的魔鬼', '国歌', '钢琴曲']


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


def music_play(text, play_time):
    """
    输入歌曲名称，让APOLLO机器人将其播放出来，实现音乐播放功能
    """
    start_res = start_music(text)
    if start_res and start_res['status'] == 0:
        print('>>> 小贝音乐播放功能打开成功 <<<')
        res = get_music_status()
        start_time = datetime.datetime.now()
        cur_time = datetime.datetime.now()
        print('------------------------------------')
        print('小贝音乐播放中.......')
        while (cur_time - start_time).seconds < play_time and res['status'] == 0:
            res = get_music_status()
            cur_time = datetime.datetime.now()
        print('------------------------------------')
        print('小贝音乐播放结束，退出程序')
        print('------------------------------------')
        return True
    else:
        return False


def music_play_by_vui_sample():
    """
    进行语音交互：唤醒 “小贝”，让其播放自己想听的歌曲，目前支持['来自天堂的魔鬼', '国歌', '钢琴曲']
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
    for music_name in MUSIC_LIST:
        # 判断支持的歌曲是否在识别的文字里
        if music_name in text_reg:
            # 播放音乐,播放时长为30s，歌曲时长不足30s的自动停止，播放时长可调
            music_play(music_name, 30)
            # 停止播放音乐
            stop_music()
            return True
    return False


if __name__ == '__main__':
    m_res = music_play_by_vui_sample()
    while not m_res:
        print('音乐播放失败，继续识别')
        m_res = music_play_by_vui_sample()
    print('音乐播放成功，退出程序')
