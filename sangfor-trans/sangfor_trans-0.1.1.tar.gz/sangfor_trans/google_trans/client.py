# -*- coding: utf-8 -*-
"""
谷歌翻译模块，可以通过该模块进行翻译.
"""
import requests
import random
import json
import traceback

from sangfor_trans.google_trans import urls, utils
from sangfor_trans.google_trans.adapters import TimeoutAdapter
from sangfor_trans.google_trans.compat import PY3
from sangfor_trans.google_trans.gtoken import TokenAcquirer
from sangfor_trans.google_trans.constants import DEFAULT_USER_AGENT, LANGCODES, LANGUAGES, SPECIAL_CASES
from sangfor_trans.google_trans.models import Translated, Detected
from sangfor_trans.config import (
    SUCCESS, SUCCESS_STATUE_CODE, EXCEPT_STATU_CODE, INVALID_DEST_LANG, 
    INVALID_SOURCE_LANG, PARAM_STATUE_CODE, INVALID_PARAMETER, LANGMAP
)


EXCLUDES = ('en', 'ca', 'fr')


class Translator(object):
    """
    谷歌翻译操作类，初始化、获取服务翻译url、翻译内容等
    """
    def __init__(self, service_urls=None, user_agent=DEFAULT_USER_AGENT, proxies=None, timeout=None):
        """
        创建会话对象，处理请求头，模拟浏览器访问
        """
        self.session = requests.Session()
        if proxies:
            self.session.proxies = proxies
        self.session.headers.update({
            'User-Agent': user_agent,
        })

        if timeout:
            self.session.mount('https://', TimeoutAdapter(timeout))
            self.session.mount('http://', TimeoutAdapter(timeout))

        self.service_urls = service_urls or [urls.SERVICE_URL]
        self.token_acquirer = TokenAcquirer(session=self.session, host=self.service_urls[0])

    def _pick_service_url(self):
        """
        获取翻译服务url
        """
        if len(self.service_urls) == 1:
            return self.service_urls[0]
        return random.choice(self.service_urls)

    def _translate(self, from_lang, to_lang, query_text ):
        """

        """
        if not PY3 and isinstance(query_text, str):  
            query_text = query_text.decode('utf-8')

        token = self.token_acquirer.do(query_text)
        params = utils.build_params(query=query_text, src=from_lang, dest=to_lang, token=token)
        url = urls.TRANSLATE.format(host=self._pick_service_url())
        r = self.session.get(url, params=params)

        data = utils.format_json(r.text)
        return data

    def _parse_extra_data(self, data):
        response_parts_name_mapping = {
            0: 'translation',
            1: 'all-translations',
            2: 'original-language',
            5: 'possible-translations',
            6: 'confidence',
            7: 'possible-mistakes',
            8: 'language',
            11: 'synonyms',
            12: 'definitions',
            13: 'examples',
            14: 'see-also',
        }
        extra = {}
        for index, category in response_parts_name_mapping.items():
            extra[category] = data[index] if (index < len(data) and data[index]) else None
        return extra

    def translate(self, from_lang, to_lang, query_text):
        """
        参数校验、翻译内容判断、格式处理、进行翻译
        return: 返回翻译结果，json格式
        """
        to_lang = to_lang.lower().split('_', 1)[0]
        from_lang = from_lang.lower().split('_', 1)[0]

        if from_lang != 'auto' and from_lang not in LANGUAGES:
            if from_lang in SPECIAL_CASES:
                from_lang = SPECIAL_CASES[from_lang]
            elif from_lang in LANGCODES:
                from_lang = LANGCODES[from_lang]
            elif from_lang in LANGMAP:
                from_lang = LANGMAP[from_lang]
            else:
                return json.dumps({'msg': INVALID_SOURCE_LANG, "statu_code": EXCEPT_STATU_CODE})

        if to_lang not in LANGUAGES:
            if to_lang in SPECIAL_CASES:
                to_lang = SPECIAL_CASES[to_lang]
            elif to_lang in LANGCODES:
                to_lang = LANGCODES[to_lang]
            elif to_lang in LANGMAP:
                to_lang = LANGMAP[to_lang]
            else:
                return json.dumps({'msg': INVALID_DEST_LANG, "statu_code": EXCEPT_STATU_CODE})

        # 翻译内容为list，则走这里进行处理
        if isinstance(query_text, list):
            result = []
            for item in query_text:
                translated = self.translate(from_lang, to_lang, item)
                result.append(translated)
            return result

        origin = query_text
        data = self._translate(from_lang, to_lang, query_text)

        # 格式处理
        translated = ''.join([d[0] if d[0] else '' for d in data[0]])

        extra_data = self._parse_extra_data(data)

        # 当from_lang=auto时，Translator将识别的实际源语言
        try:
            from_lang = data[2]
        except Exception:  
            traceback.print_exc()

        pron = origin
        try:
            pron = data[0][1][-2]
        except Exception:  
            traceback.print_exc()
        if not PY3 and isinstance(pron, unicode) and isinstance(origin, str):  
            origin = origin.decode('utf-8')
        if to_lang in EXCLUDES and pron == origin:
            pron = translated

        # 兼容Python2
        if not PY3:  
            if isinstance(from_lang, str):
                from_lang = from_lang.decode('utf-8')
            if isinstance(to_lang, str):
                to_lang = to_lang.decode('utf-8')
            if isinstance(translated, str):
                translated = translated.decode('utf-8')

        # 最后结果值处理输出成Translated对象格式
        result = Translated(src=from_lang, dest=to_lang, origin=origin,
                            text=translated, pronunciation=pron, extra_data=extra_data).text
        if result:
            ret_list = [{u'src': query_text.decode("utf-8"), u'dst': result}]
            trans_result = {'msg': SUCCESS, 'statu_code': SUCCESS_STATUE_CODE, 'from': from_lang, 'to': to_lang, 'trans_result': ret_list}
        else:
            trans_result = {'msg': INVALID_QUERY_TEXT, 'statu_code': PARAM_STATUE_CODE}
        return json.dumps(trans_result)

    def detect(self, query_text):
        """
        检测翻译内容属于哪种语言
        """
        if isinstance(query_text, list):
            result = []
            for item in query_text:
                lang = self.detect(item)
                result.append(lang)
            return result

        data = self._translate(from_lang='auto', to_lang='en', query_text=query_text)

        from_lang = ''
        confidence = 0.0
        try:
            from_lang = ''.join(data[8][0])
            confidence = data[8][-2][0]
        except Exception:  
            trackback.print_exc()
        result = Detected(lang=from_lang, confidence=confidence)

        return result
