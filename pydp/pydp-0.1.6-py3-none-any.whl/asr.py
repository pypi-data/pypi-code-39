#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: ASR.py
Desc: 语音识别
"""
from aip import AipSpeech
import os
import logging
import requests
import base64
import hashlib
import time
import json
from abc import ABCMeta, abstractmethod
from dp import utils, audio, constants
from dp.speech import TencentSpeech, AliSpeech
from dp.snowboy import snowboydecoder


def get_engine(slug, profile):
    """
    获取asr引擎
    :param slug: 引擎名（baidu-asr、xunfei-asr、ali-asr、tencent-asr）
    :param profile: 引擎配置（{
        'appid': '967064',
        'api_key': 'qg4haN8xxx',   # API Key
        'secret_key': 'xxx',
        'per': 1,  # 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫
        'lan': 'zh',
    }）
    :returns: asr engine
    """

    if not slug or type(slug) is not str:
        raise TypeError("无效的 ASR slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                                   engine.SLUG == slug, _get_engine_list()))

    if len(selected_engines) == 0:
        raise ValueError("错误：找不到名为 {} 的 ASR 引擎".format(slug))
    else:
        if len(selected_engines) > 1:
            logging.warning("注意: 有多个 ASR 名称与指定的引擎名 {} 匹配").format(slug)
        engine = selected_engines[0]
        logging.info("使用 {} ASR 引擎".format(engine.SLUG))
        return engine.get_instance(profile)


def _get_engine_list():
    """
    支持的tts引擎列表

    :returns: engine list
    """
    def get_subclasses(cls):
        subclasses = set()
        for subclass in cls.__subclasses__():
            subclasses.add(subclass)
            subclasses.update(get_subclasses(subclass))
        return subclasses
    return [engine for engine in
            list(get_subclasses(AbstractASR))
            if hasattr(engine, 'SLUG') and engine.SLUG]


class AbstractASR(object):
    """
    asr引擎抽象类
    """

    __metaclass__ = ABCMeta

    def __init__(self):
        """初始化"""
        self.listening = ''  # 是否正在收音

    '''@classmethod
    def get_config(cls):
        return {}'''

    @classmethod
    def get_instance(cls, profile):
        """
        返回实例对象

        :param profile: 实例参数
        :returns: instance
        """
        #profile = cls.get_config()
        instance = cls(**profile)
        return instance

    @abstractmethod
    def transcribe(self, video_file):
        """
        语音识别

        :param video_file: 音频文件
        :returns: 识别出的文本
        """
        pass

    def listen(self, hotword_model=None, silent_threshold=15, recording_timeout=10):
        """
        从话筒收音并识别为文字

        :param hotword_model: 唤醒词模型文件地址
        :param silent_threshold: 判断为静音的阈值（默认15）。环境比较吵杂的地方可以适当调大
        :param recording_timeout: 录制的语音最大长度（默认5秒）
        :returns: 话筒收音文本
        """
        if self.listening == '':
            self.listening = str(int(time.time()))
        if not hotword_model:
            hotword_model = constants.DATA_PATH + '/hotword/小白.pmdl'
        logging.info("hotword_model: {}".format(hotword_model))

        audio.play(media='on.wav')
        listener = snowboydecoder.ActiveListener([hotword_model])
        voice_file = listener.listen(
            silent_count_threshold=silent_threshold,
            recording_timeout=recording_timeout * 4
        )
        audio.play(media='off.wav')
        phrase = self.transcribe(voice_file)
        utils.rm(voice_file)
        logging.info("listen: {}".format(phrase))
        self.listening = ''
        return phrase


class BaiduASR(AbstractASR):
    """
    百度的语音识别API.
    dev_pid:
        - 1936: 普通话远场
        - 1536：普通话(支持简单的英文识别)
        - 1537：普通话(纯中文识别)
        - 1737：英语
        - 1637：粤语
        - 1837：四川话
    要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
    之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
    填入 config.xml 中.
    ...
        baidu_yuyin: 
            appid: '9670645'
            api_key: 'qg4haN8b2bGvFtCbBGqhrmZy'
            secret_key: '585d4eccb50d306c401d7df138bb02e7'
        ...
    """

    SLUG = "baidu-asr"

    def __init__(self, appid, api_key, secret_key, dev_pid=1936, **args):
        super(self.__class__, self).__init__()
        self.client = AipSpeech(appid, api_key, secret_key)
        self.dev_pid = dev_pid

    '''@classmethod
    def get_config(cls):
        # Try to get baidu_yuyin config from config
        return config.get('baidu_yuyin', {})'''

    def transcribe(self, video_file):
        """
        语音识别

        :param video_file: 音频文件
        :returns: 识别出的文本
        """
        # 识别本地文件
        pcm = audio.get_pcm(video_file)
        res = self.client.asr(pcm, 'pcm', 16000, {
            'dev_pid': self.dev_pid,
        })
        if res['err_no'] == 0:
            logging.info('{} 语音识别到了：{}'.format(self.SLUG, res['result']))
            return ''.join(res['result'])
        else:
            logging.info('{} 语音识别出错了: {}'.format(self.SLUG, res['err_msg']))
            return ''


class TencentASR(AbstractASR):
    """
    腾讯的语音识别API.
    """

    SLUG = "tencent-asr"

    def __init__(self, appid, secretid, secret_key, region='ap-guangzhou', **args):
        super(self.__class__, self).__init__()
        self.engine = TencentSpeech.tencentSpeech(secret_key, secretid)
        self.region = region

    '''@classmethod
    def get_config(cls):
        # Try to get tencent_yuyin config from config
        return config.get('tencent_yuyin', {})'''

    def transcribe(self, video_file):
        """
        语音识别

        :param video_file: 音频文件
        :returns: 识别出的文本
        """
        mp3_path = video_file
        if utils.get_ext(video_file) == '.wav':
            mp3_path = audio.convert_wav_to_mp3(video_file)
        r = self.engine.ASR(mp3_path, 'mp3', '1', self.region)
        res = json.loads(r)
        if 'Response' in res and 'Result' in res['Response']:
            logging.info('{} 语音识别到了：{}'.format(self.SLUG, res['Response']['Result']))
            return res['Response']['Result']
        else:
            logging.critical('{} 语音识别出错了'.format(self.SLUG), exc_info=True)
            return ''


class XunfeiASR(AbstractASR):
    """
    科大讯飞的语音识别API.
    外网ip查询：https://ip.51240.com/
    """

    SLUG = "xunfei-asr"

    def __init__(self, appid, api_key):
        super(self.__class__, self).__init__()
        self.appid = appid
        self.api_key = api_key

    '''@classmethod
    def get_config(cls):
        # Try to get xunfei_yuyin config from config
        return config.get('xunfei_yuyin', {})'''

    def getHeader(self, aue, engineType):
        curTime = str(int(time.time()))
        # curTime = '1526542623'
        param = "{\"aue\":\"" + aue + "\"" + ",\"engine_type\":\"" + engineType + "\"}"
        logging.debug("param:{}".format(param))
        paramBase64 = str(base64.b64encode(param.encode('utf-8')), 'utf-8')
        logging.debug("x_param:{}".format(paramBase64))

        m2 = hashlib.md5()
        m2.update((self.api_key + curTime + paramBase64).encode('utf-8'))
        checkSum = m2.hexdigest()
        header = {
            'X-CurTime': curTime,
            'X-Param': paramBase64,
            'X-Appid': self.appid,
            'X-CheckSum': checkSum,
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header

    def getBody(self, filepath):
        binfile = open(filepath, 'rb')
        data = {'audio': base64.b64encode(binfile.read())}
        return data

    def transcribe(self, video_file):
        """
        语音识别

        :param video_file: 音频文件
        :returns: 识别出的文本
        """
        if utils.get_ext(video_file) == '.mp3':
            video_file = audio.convert_mp3_to_wav(video_file)
        URL = "http://api.xfyun.cn/v1/service/v1/iat"
        r = requests.post(URL, headers=self.getHeader('raw', 'sms16k'), data=self.getBody(video_file))
        res = json.loads(r.content.decode('utf-8'))
        logging.debug(res)
        if 'code' in res and res['code'] == '0':
            logging.info('{} 语音识别到了：{}'.format(self.SLUG, res['data']))
            return res['data']
        else:
            logging.critical('{} 语音识别出错了'.format(self.SLUG), exc_info=True)
            return ''


class AliASR(AbstractASR):
    """
    阿里的语音识别API.
    """

    SLUG = "ali-asr"

    def __init__(self, appKey, token, **args):
        super(self.__class__, self).__init__()
        self.appKey, self.token = appKey, token

    '''@classmethod
    def get_config(cls):
        # Try to get ali_yuyin config from config
        return config.get('ali_yuyin', {})'''

    def transcribe(self, video_file):
        """
        语音识别

        :param video_file: 音频文件
        :returns: 识别出的文本
        """
        if utils.get_ext(video_file) == '.mp3':
            video_file = audio.convert_mp3_to_wav(video_file)
        result = AliSpeech.asr(self.appKey, self.token, video_file)
        if result is not None:
            logging.info('{} 语音识别到了：{}'.format(self.SLUG, result))
            return result
        else:
            logging.critical('{} 语音识别出错了'.format(self.SLUG), exc_info=True)
            return ''


if __name__ == '__main__':
    """test"""
    # log init
    utils.init_logging(log_file='asr', log_path=constants.APP_PATH)

    # 初始化语音识别
    profile = {
        'appid': '1253537070',
        'secretid': 'AKID7C7JK9QomcWJUjcsKbK8iLQjhju8fC3z',
        'secret_key': '2vhKRVSn4mXQ9PiT7eOtBqQhR5Z6IvPn',
        'region': 'ap-guangzhou',  # 服务地区，有效值：http://suo.im/4EEQYD
        'voiceType': 0,            # 0: 女声1；1：男生1；2：男生2
        'language': 1,             # 1: 中文；2：英文
    }
    asr = get_engine('tencent-asr', profile)

    # 识别为文本
    phrase = asr.transcribe('/tmp/tts/7eca689f0d3389d9dea66ae112e5cfd7.mp3')
    print(phrase)
    '''
    # 监听话筒并识别为文字
    phrase = asr.listen(recording_timeout=15)
    print(phrase)
    '''
