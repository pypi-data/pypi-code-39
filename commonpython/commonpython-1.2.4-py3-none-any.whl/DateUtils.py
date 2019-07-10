#!usr/bin/env python
#-*- coding:utf-8 _*-
"""
@file: DateUtils.py
@time: 2019/05/16
"""
import time,datetime

class DateUtils(object):

    def unix_millisecond(self):
        '''时间戳，毫秒
        '''
        return int(time.time() * 1000)

    def unix_second(self):
        '''时间戳，秒'''
        return int(time.time())

    def in_hours(self,hour=-1):
        '''
        最近几小时，提前传负数
        :param hour:
        :return:
        '''
        return (datetime.datetime.now() + datetime.timedelta(hours=hour)).strftime("%Y-%m-%d %H:%M:%S")

    def in_days(self,day=-1):
        '''
        最近几天，提前传负数
        :param day:
        :return:
        '''
        return (datetime.datetime.now() + datetime.timedelta(days=day)).strftime("%Y-%m-%d %H:%M:%S")

    def in_minutes(self,minute=-1):
        '''
        最近几分钟，提前传负数
        :param day:
        :return:
        '''
        return (datetime.datetime.now() + datetime.timedelta(minutes=minute)).strftime("%Y-%m-%d %H:%M:%S")


if __name__ == '__main__':
    print(DateUtils().in_minutes())
