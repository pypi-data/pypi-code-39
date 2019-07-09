#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@file: HttpUtils.py
@time: 2019/07/09
"""
import requests
from commonpython.DateUtils import DateUtils

class HttpUtils(object):
    '''链式调用'''
    def __init__(self,url):
        self.url = url
        self.session = requests.session()

    def setData(self,data):
        '''
        设置data
        :param data:  dict
        :return:
        '''
        self.data = data
        return self

    def setHeader(self,header):
        '''
        设置header
        :param data:  dict
        :return:
        '''
        self.header = header
        return self

    def get(self):
        '''
        get方法
        :return:  有参数调用setData
        '''
        res_obj = self.session.get(url=self.url,params=self.data)
        return res_obj

    def post(self):
        '''
        post请求，根据Content-Type判断参数格式
        :return:
        '''
        if 'application/json' in self.header.get('Content-Type',''):
            res_obj = self.session.post(url=self.url,json=self.data,headers=self.header)
        else:
            res_obj = self.session.post(url=self.url, data=self.data, headers=self.header)
        return res_obj

    def start(self,method):
        '''
        调用入口
        :param method:   方法
        :return:  调用对象,响应时间,单位毫秒(ms)
        '''
        if hasattr(self,method):
            start_time = DateUtils().unix_millisecond()
            res_obj = getattr(self,method)()
            end_time = DateUtils().unix_millisecond()
            run_time = end_time - start_time
            return res_obj,run_time
        else:
            return 'method is not allow'

if __name__ == '__main__':
    res = HttpUtils("http://xxx:9000/taskapi/TobRiskResult").setData({"testdata":"testdata"}).setHeader({"testhe":"testhe"}).start('get')
    print(res[0].text,res[1])