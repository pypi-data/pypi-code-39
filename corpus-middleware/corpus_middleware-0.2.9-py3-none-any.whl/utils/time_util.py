#!/usr/bin/env python
# -*- coding: utf-8 -*-

import time
import datetime


class TimeUtil:
    @staticmethod
    def time_stamp_formatter(time_stamp):
        time_local = time.localtime(time_stamp)
        formatter_time = time.strftime("%Y-%m-%d %H:%M:%S", time_local)
        # logger.info(f"{time_stamp} {formatter_time}")
        return formatter_time

    @staticmethod
    def data_time_valid_and_formatter(data_time):
        try:
            if ":" in data_time:
                data_time = time.strptime(data_time, "%Y-%m-%d %H:%M:%S")
            else:
                data_time = time.strptime(data_time, "%Y-%m-%d")
            return time.strftime("%Y-%m-%d %H:%M:%S", data_time)
        except:
            return False

    @staticmethod
    def date_compare(date_time1, date_time2):
        date_time1 = datetime.datetime.strptime(date_time1, "%Y-%m-%d %H:%M:%S")
        date_time2 = datetime.datetime.strptime(date_time2, "%Y-%m-%d %H:%M:%S")
        if date_time1 > date_time2:
            return 1
        elif date_time1 < date_time2:
            return -1
        elif date_time1 == date_time2:
            return 0


def mtime():
    t = time.time()
    return int(t)


if __name__ == "__main__":
    import os

    # print(TimeUtil.time_stamp_formatter('2019-7-7 16:35:58'))
    # print(os.path.getctime('D:\Temp\corpus-middleware\localFileStorage\经济犯罪.docx'))
    # print(mtime())
    # print("time.localtime() : {}".format(time.localtime()))

    # print(date_compare('2017-03-01 00:00:00', '2017-05-11 00:00:00'))
    # print(TimeUtil.data_time_formatter('2017-03-01 '))
