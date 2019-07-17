#!usr/bin/env python
# coding=utf-8
from robot.api import logger
from robot.api.deco import keyword
import hashlib
import time
from .version import VERSION


__author__ = 'bryan hou'
__email__ = 'bryanhou@gmail.com'
__version__ = VERSION

class MyKeywords(object):

    @keyword('Located User')
    def located_user(self,value):
        """落库地址查询"""
        relation_dict = {(1,251):"1", (251,501):"1", (501,751):"1", (751,1001):"1"}
        
        digest = int(hashlib.md5(str(value).encode()).hexdigest(), 16)
        mod = digest % 1000 + 1
        for k, v in relation_dict.items():
            if k[0]<=mod<k[1]:
                returns = str(digest % 32 + 1).zfill(2)
                return returns
    
    @keyword('Get Current Time')                
    def get_current_time(self):
        """获取当前时间"""
        current_time = time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time()))
        return current_time

    @keyword('Unicode To Dict')                
    def uinicode_to_dict(self,input):
        """获取当前时间"""
        inputStr = str(input)
        inputDict = json.loads(inputStr)
        return inputDict

    @keyword('GBK To Unicode')                
    def convert_gbk_2_unicode(self,input):
        """获取当前时间"""
        output = str(input).encode('unicode_escape')
        return output

    @keyword('Unicode To GBK')                
    def convert_unicode_2_gbk(self,input):
        # """Linux"""
        output = str(input).encode('utf-8').decode('unicode_escape')
        # """Windows"""
        # output = str(input).encode('unicode_escape').decode('unicode_escape')
        return output