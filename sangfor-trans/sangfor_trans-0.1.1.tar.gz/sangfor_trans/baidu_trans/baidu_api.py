#/usr/bin/env python
# -*- coding:utf-8 -*-
import httplib
import md5
import urllib
import random
import traceback
import json

from sangfor_trans.baidu_trans.setting import (
    API_URL, APP_ID, BASE_URL, SECRET_KEY, LANGUAGES, STATU_CODE_MAP, RANDOM_LOW, RANDOM_UP
    )
from sangfor_trans.config import (
    SUCCESS_STATUE_CODE, EXCEPT_STATU_CODE, SUCCESS, INVALID_SOURCE_LANG, INVALID_DEST_LANG, 
    LANGMAP, LANGMAP_REVERSED
)


class Translator(object):
    """
    百度翻译操作类
    """
    def __init__(self):
       pass

    def translate(self, from_lang, to_lang, query_text):
        """
        百度翻译api入口
        from_lang:  源语言
        to_lang:    译文语言
        query_text: 翻译文本
        return：    返回翻译结果
        """
        from_lang = from_lang.lower().strip()
        to_lang = to_lang.lower().strip()
        if from_lang not in LANGUAGES:
            if from_lang in LANGMAP_REVERSED:
                from_lang = LANGMAP_REVERSED[from_lang]
            else:
                return json.dumps({'msg': INVALID_SOURCE_LANG, 'statu_code': EXCEPT_STATU_CODE})

        if to_lang not in LANGUAGES:
            if to_lang in LANGMAP_REVERSED:
                to_lang = LANGMAP_REVERSED[to_lang]
            else:
                return json.dumps({'msg': INVALID_DEST_LANG, 'statu_code': EXCEPT_STATU_CODE})

        httpClient = None
        url = self.get_url(from_lang, to_lang, query_text)
        try:
            # API HTTP请求
            httpClient = httplib.HTTPConnection(BASE_URL)
            httpClient.request('GET', url)
        
            # 创建HTTPResponse对象
            response = httpClient.getresponse()
            resp = response.read()

            result = json.loads(resp)
            # 错误码和错误信息处理
            if "error_code" not in result:
                result["statu_code"] = SUCCESS_STATUE_CODE
                result["msg"] = SUCCESS
            else:
                if result["error_code"] in STATU_CODE_MAP:
                    result["statu_code"] = STATU_CODE_MAP.get(result["error_code"])
                else:
                    result["statu_code"] = EXCEPT_STATU_CODE
                result["msg"] = result["error_msg"]
                del result["error_code"]
                del result["error_msg"]
            
            return json.dumps(result)
             
        except Exception as e:
            traceback.print_exc()
        finally:
            if httpClient:
                httpClient.close()

    @staticmethod
    def get_url(from_lang, to_lang, query_text):
        """
        生成请求url
        """
        # 随机生成数据
        salt = random.randint(RANDOM_LOW, RANDOM_UP)
        # MD5生成签名
        sign = APP_ID + query_text + str(salt) + SECRET_KEY
        m1 = md5.new()
        m1.update(sign)
        sign = m1.hexdigest()
        # 拼接URL
        url = API_URL +'?appid=' + APP_ID + '&q=' + urllib.quote(query_text) + '&from=' + from_lang + '&to=' + to_lang + '&salt=' + str(salt) + '&sign=' + sign
        return url

