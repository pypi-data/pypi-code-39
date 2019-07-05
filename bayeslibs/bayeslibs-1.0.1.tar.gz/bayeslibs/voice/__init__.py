# conding=utf-8
"""
@project:bayeslibs
@language:Python3
@create:2019/5/30
@author:qianyang<qianyang@aibayes.com>
@description:none
"""
from .chat.small_talk import start_small_talk, stop_small_talk
from .music.music import start_music, stop_music, get_music_status
from .speak.tts import start_speak, stop_speak, get_speak_status
from .speech.acr import open_acr, close_acr, get_acr_status
from .speech.asr import open_asr, close_asr, get_asr_status
from .wakeup.wts import open_wakeup, close_wakeup, get_wakeup_status
