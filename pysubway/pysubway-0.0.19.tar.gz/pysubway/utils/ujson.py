# -*- coding: utf-8 -*-

import json
from datetime import date
from datetime import datetime


class ComplexEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, datetime):
            return obj.strftime('%Y-%m-%d %H:%M:%S')
        elif isinstance(obj, date):
            return obj.strftime('%Y-%m-%d')
        else:
            return json.JSONEncoder.default(self, obj)


def dumps(py_ins):
    u"""
    把 py_ins 转化为 json 字符串对象;
    这个封装方法的优势：
    + sort_keys=True，避免 dict 对象转化为 json str 时因位置不同导致 json 不同；
    + 支持 datatime 的转化；
    :param py_ins:
    :return:
    """
    return json.dumps(py_ins, sort_keys=True, cls=ComplexEncoder)
