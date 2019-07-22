# -*- coding:utf-8 -*-
import json

from sangfor_trans.baidu_trans import baidu_api
from sangfor_trans.google_trans import client
from sangfor_trans.config import (
    GOOGLE, BAIDU, EXCEPT_STATU_CODE, INVALID_TRANS_TYPE, INVALID_PARAMETER, PARAM_STATUE_CODE
)


class GetTranslator(object):
    def __init__(self, trans_type):
        self.trans_type = trans_type

    def translate(self, from_lang, to_lang, query_text):
        trans_result = {}
        # 判读传入字段是否为空
        if not from_lang or not to_lang or not query_text:
            trans_result["statu_code"] = PARAM_STATUE_CODE
            trans_result["msg"] = INVALID_PARAMETER
            return json.dumps(trans_result)

        if not isinstance(query_text, list):
            query_text = query_text.replace("\n", "")

        if self.trans_type == BAIDU:
            translator = baidu_api.Translator()
        elif self.trans_type == GOOGLE:
            # translator = client.Translator(service_urls=["translate.google.cn"])
            translator = client.Translator()
        else:
            trans_result["statu_code"] = PARAM_STATUE_CODE
            trans_result["msg"] = INVALID_TRANS_TYPE
            return json.dumps(trans_result)

        trans_result = translator.translate(from_lang, to_lang, query_text)

        return trans_result
            
