#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
File: tts.py
Desc: 语音合成
"""
from aip import AipSpeech
import os
import logging
import base64
import time
import requests
import hashlib
from abc import ABCMeta, abstractmethod
from dp import utils, constants, audio
from dp.speech import TencentSpeech, AliSpeech


def get_engine(slug, profile, cache_path=''):
    """
    获取tts引擎

    :param slug: 引擎名（baidu-tts、xunfei-tts、ali-tts、tencent-tts）
    :param profile: 引擎配置（{
        'appid': '967064',
        'api_key': 'qg4haN8xxx',   # API Key
        'secret_key': 'xxx',
        'per': 1,  # 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫
        'lan': 'zh',
    }）
    :param cache_path: 合成音频cache位置（为空表示不cache）
    :returns: tts engine
    """

    if not slug or type(slug) is not str:
        raise TypeError("无效的 tts slug '%s'", slug)

    selected_engines = list(filter(lambda engine: hasattr(engine, "SLUG") and
                                   engine.SLUG == slug, _get_engine_list()))

    if len(selected_engines) == 0:
        raise ValueError("错误：找不到名为 {} 的 tts 引擎".format(slug))
    else:
        if len(selected_engines) > 1:
            logging.warning("注意: 有多个 tts 名称与指定的引擎名 {} 匹配").format(slug)
        engine = selected_engines[0]
        logging.info("使用 {} tts 引擎".format(engine.SLUG))
        return engine.get_instance(profile, cache_path)


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
            list(get_subclasses(AbstractTTS))
            if hasattr(engine, 'SLUG') and engine.SLUG]


class AbstractTTS(object):
    """
    tts引擎抽象类
    """
    __metaclass__ = ABCMeta

    def __init__(self):
        """初始化"""
        self.saying = ''  # 是否正在说话
        self.cache_path = ''  # 合成音频cache位置（为空表示不cache）

    def set_cache_path(self, cache_path):
        """
        设置cache参数

        :param cache_path: 合成音频cache位置（为空表示不cache）
        :returns: 
        """
        self.cache_path = cache_path

    '''@classmethod
    def get_config(cls):
        return {}'''

    @classmethod
    def get_instance(cls, profile=None, cache_path=''):
        """
        返回实例对象

        :param profile: 实例参数
        :param cache_path: 合成音频cache位置（为空表示不cache）
        :returns: instance
        """
        #profile = cls.get_config()
        instance = cls(**profile)
        instance.set_cache_path(cache_path)
        return instance

    @abstractmethod
    def get_speech(self, phrase):
        """
        合成声音

        :param phrase: 要合成的文本
        :returns: 合成的音频文件地址
        """
        pass

    def say(self, phrase, callback=None, force_update=False):
        """
        说话（合成声音并播放）

        :param phrase: 要说的话
        :param force_update: 是否强制更新cache
        :param callback: 播放完毕后的回调函数
        :returns: 
        """
        logging.info("saying: " + phrase)
        self.saying = phrase

        # get cache
        voice_file = self._get_cache(phrase, self.cache_path, force_update)

        # 合成声音
        if not voice_file:
            voice_file = self.get_speech(phrase)

            # set cache
            cache_file = self._set_cache(phrase, self.cache_path, voice_file)
            if cache_file:
                voice_file = cache_file

        def _callback():
            if callback is not None:
                self.say_callback(phrase)
                return callback(phrase)
            else:
                return self.say_callback(phrase)
        audio.play(voice_file, delete=not self.cache_path, callback=_callback)

    def say_callback(self, phrase):
        """
        默认说话完毕的回调

        :param phrase: 要说的话
        :returns: 
        """
        self.saying = ''

    @classmethod
    def _get_cache(cls, phrase, cache_path, force_update):
        """
        获取语音cache文件位置

        :param phrase: 要合成的文本
        :param cache_path: cache位置
        :param force_update: 是否强制更新cache
        :returns: cache文件地址
        """
        if cache_path != '' and force_update is False:
            utils.mkdir(cache_path)
            cache_file = os.path.join(cache_path, utils.md5(phrase)+'.mp3')
            if os.path.exists(cache_file):
                logging.info('get cache! {} {}'.format(phrase, cache_file))
                return cache_file
        return ''

    @classmethod
    def _set_cache(cls, phrase, cache_path, tmpfile):
        """
        保存语音文件cache

        :param phrase: 要合成的文本
        :param cache_path: cache位置
        :param tmpfile: 需要cache的临时音频文件
        :returns: 保存的cache文件地址"""
        if cache_path != '' and os.path.exists(tmpfile):
            cache_file = os.path.join(cache_path, utils.md5(phrase)+'.mp3')
            utils.rm(cache_file)
            ret = utils.mv(tmpfile, cache_file)
            if ret:
                logging.info('set cache! {} {}'.format(phrase, cache_file))
                return cache_file
        return ''


class BaiduTTS(AbstractTTS):
    """
    使用百度语音合成技术
    要使用本模块, 首先到 yuyin.baidu.com 注册一个开发者账号,
    之后创建一个新应用, 然后在应用管理的"查看key"中获得 API Key 和 Secret Key
    填入 config.yml 中.
    ...
        baidu_yuyin: 
            appid: '9670645'
            api_key: 'qg4haN8b2bGvFtCbBGqhrmZy'
            secret_key: '585d4eccb50d306c401d7df138bb02e7'
            dev_pid: 1936
            per: 1
            lan: 'zh'
        ...
    """

    SLUG = "baidu-tts"

    def __init__(self, appid, api_key, secret_key, per=1, lan='zh', **args):
        super(self.__class__, self).__init__()
        self.client = AipSpeech(appid, api_key, secret_key)
        self.per, self.lan = str(per), lan

    '''@classmethod
    def get_config(cls):
        # Try to get baidu_yuyin config from config
        return config.get('baidu_yuyin', {})'''

    def get_speech(self, phrase):
        """
        合成声音

        :param phrase: 要合成的文本
        :returns: 合成的音频文件地址
        """
        result = self.client.synthesis(phrase, self.lan, 1, {'per': self.per})
        # 识别正确返回语音二进制 错误则返回dict
        if isinstance(result, dict):
            logging.critical('{} 合成失败！'.format(self.SLUG), exc_info=True)
            return None

        # 合成文件
        tmpfile = utils.write_temp_file(result, '.mp3')
        logging.info('{} 语音合成成功，合成路径：{}'.format(self.SLUG, tmpfile))
        return tmpfile


class TencentTTS(AbstractTTS):
    """
    腾讯的语音合成
    region: 服务地域，挑个离自己最近的区域有助于提升速度。
        有效值：https://cloud.tencent.com/document/api/441/17365#.E5.9C.B0.E5.9F.9F.E5.88.97.E8.A1.A8
    voiceType:
        - 0：女声1，亲和风格(默认)
        - 1：男声1，成熟风格
        - 2：男声2，成熟风格
    language:
        - 1: 中文，最大100个汉字（标点符号算一个汉子）
        - 2: 英文，最大支持400个字母（标点符号算一个字母）
    """

    SLUG = "tencent-tts"

    def __init__(self, appid, secretid, secret_key, region='ap-guangzhou', voiceType=0, language=1, **args):
        super(self.__class__, self).__init__()
        self.engine = TencentSpeech.tencentSpeech(secret_key, secretid)
        self.region, self.voiceType, self.language = region, voiceType, language

    '''@classmethod
    def get_config(cls):
        # Try to get tencent_yuyin config from config
        return config.get('tencent_yuyin', {})'''

    def get_speech(self, phrase, cache_path='', force_update=False):
        """
        合成声音

        :param phrase: 要合成的文本
        :param cache_path: cache位置
        :param force_update: 是否强制更新cache
        :returns: 合成的音频文件地址
        """
        # 语音合成
        result = self.engine.tts(phrase, self.voiceType, self.language, self.region)
        if 'Response' in result and 'Audio' in result['Response']:
            audio = result['Response']['Audio']
            data = base64.b64decode(audio)
            tmpfile = utils.write_temp_file(data, '.wav')
        else:
            logging.critical('{} 合成失败！'.format(self.SLUG), exc_info=True)
            return None

        logging.info('{} 语音合成成功，合成路径：{}'.format(self.SLUG, tmpfile))
        return tmpfile


class XunfeiTTS(AbstractTTS):
    """
    科大讯飞的语音识别API.
    外网ip查询：https://ip.51240.com/
    voice_name: https://www.xfyun.cn/services/online_tts
    """

    SLUG = "xunfei-tts"

    def __init__(self, appid, api_key, voice_name='xiaoyan'):
        super(self.__class__, self).__init__()
        self.appid, self.api_key, self.voice_name = appid, api_key, voice_name

    '''@classmethod
    def get_config(cls):
        # Try to get xunfei_yuyin config from config
        return config.get('xunfei_yuyin', {})'''

    def get_speech(self, phrase, cache_path='', force_update=False):
        """
        合成声音

        :param phrase: 要合成的文本
        :param cache_path: cache位置
        :param force_update: 是否强制更新cache
        :returns: 合成的音频文件地址
        """
        URL = "http://api.xfyun.cn/v1/service/v1/tts"
        r = requests.post(URL, headers=self._get_header('lame'), data={'text': phrase})
        contentType = r.headers['Content-Type']
        if contentType == "audio/mpeg":
            tmpfile = utils.write_temp_file(r.content, '.mp3')
        else:
            logging.critical('{} 合成失败！{}'.format(self.SLUG, r.text), exc_info=True)
            return None

        logging.info('{} 语音合成成功，合成路径：{}'.format(self.SLUG, tmpfile))
        return tmpfile

    def _get_header(self, aue):
        curTime = str(int(time.time()))
        # curTime = '1526542623'
        param = "{\"aue\":\""+aue+"\",\"auf\":\"audio/L16;rate=16000\",\"voice_name\":\"" + self.voice_name + "\",\"engine_type\":\"intp65\"}"
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
            'X-Real-Ip': '127.0.0.1',
            'Content-Type': 'application/x-www-form-urlencoded; charset=utf-8',
        }
        return header


class AliTTS(AbstractTTS):
    """
    阿里的TTS
    voice: 发音人，默认是 xiaoyun
        全部发音人列表：https://help.aliyun.com/document_detail/84435.html?spm=a2c4g.11186623.2.24.67ce5275q2RGsT
    """
    SLUG = "ali-tts"

    def __init__(self, appKey, token, voice='xiaoyun', **args):
        super(self.__class__, self).__init__()
        self.appKey, self.token, self.voice = appKey, token, voice

    '''@classmethod
    def get_config(cls):
        # Try to get ali_yuyin config from config
        return config.get('ali_yuyin', {})'''

    def get_speech(self, phrase, cache_path='', force_update=False):
        """
        合成声音

        :param phrase: 要合成的文本
        :param cache_path: cache位置
        :param force_update: 是否强制更新cache
        :returns: 合成的音频文件地址
        """
        tmpfile = AliSpeech.tts(self.appKey, self.token, self.voice, phrase)
        if tmpfile is None:
            logging.critical('{} 合成失败！'.format(self.SLUG), exc_info=True)
            return None

        logging.info('{} 语音合成成功，合成路径：{}'.format(self.SLUG, tmpfile))
        return tmpfile


if __name__ == '__main__':
    """test"""
    # log init
    utils.init_logging(log_file='tts', log_path=constants.APP_PATH)

    phrase = '你好，风暴降生的丹妮莉丝，安达尔人/罗伊纳人及先民的女王、七国统治者兼全境守护、大草海的卡丽熙、龙之母、不焚者、龙石岛公主、镣铐破碎者、弥莎/弥林的女王'

    # 初始化语音合成
    profile = {
        'appid': '9670645',
        'api_key': 'qg4haN8b2bGvFtCbBGqhrmZy',   # 请改为自己的百度语音APP的API Key
        'secret_key': '585d4eccb50d306c401d7df138bb02e7',
        'per': 4,  # 发音人选择 0：女生；1：男生；3：度逍遥；4：度丫丫
        'lan': 'zh',
    }
    tts = get_engine('baidu-tts', profile, cache_path=constants.TEMP_PATH + '/tts/')
    '''
    # 合成音频文件
    video_file = tts.get_speech(phrase)
    print(video_file)
    # 播放
    audio.play(video_file)  # , delete=True)
    '''
    # 说话
    def callback(phrase):
        print("say done!")
    tts.say('你好', callback=callback, force_update=True)
