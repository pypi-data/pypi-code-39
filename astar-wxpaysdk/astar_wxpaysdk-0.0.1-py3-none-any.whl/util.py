#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Author: 河北雪域网络科技有限公司 A.Star
# @contact: astar@snowland.ltd
# @site: www.snowland.ltd
# @file: util.py
# @time: 2019/7/3 15:12
# @Software: PyCharm


__author__ = 'A.Star'

from bs4 import BeautifulSoup
from pysmx.crypto import hashlib


def get_sign(data_dict, key, sign_type='MD5'):
    """
    签名函数
    :param data_dict: 数据
    :param key: 密钥
    :param sign_type: 签名方法
    :return:
    """
    params_list = sorted(data_dict.items(), key=lambda e: e[0], reverse=False)  # 参数字典倒排序为列表
    params_str = "&".join(u"{}={}".format(k, v) for k, v in params_list) + '&key=' + key
    # 组织参数字符串并在末尾添加商户交易密钥
    if sign_type == 'MD5':
        md5 = hashlib.md5()  # 使用MD5加密模式
        md5.update(params_str.encode('utf-8'))  # 将参数字符串传入
        sign = md5.hexdigest().upper()  # 完成加密并转为大写
        return sign
    else:
        return None


def trans_dict_to_xml(data_dict: dict):
    """
    定义字典转XML的函数
    :param data_dict:
    :return:
    """
    data_xml = []
    sorted_data_dict = sorted(data_dict.items())
    for k, v in sorted_data_dict:  # 遍历字典排序后的key
        if k == 'detail' and not v.startswith('<![CDATA['):  # 添加XML标记
            v = '<![CDATA[{}]]>'.format(v)
        data_xml.append('<{key}>{value}</{key}>'.format(key=k, value=v))
    return '<xml>{}</xml>'.format(''.join(data_xml)).encode('utf-8')  # 返回XML，并转成utf-8，解决中文的问题


def trans_xml_to_dict(data_xml):
    """
    xml转换到dict的方法
    :param data_xml:
    :return:
    """
    soup = BeautifulSoup(data_xml, features='xml')
    xml = soup.find('xml')  # 解析XML
    if not xml:
        return {}
    data_dict = dict([(item.name, item.text) for item in xml.find_all()])
    return data_dict
