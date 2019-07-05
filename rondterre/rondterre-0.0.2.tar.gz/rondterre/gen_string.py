# -*- coding: utf-8 -*-
import time


def gen_time_string():
    res_ = time.strftime('%Y%m%d%H%M%S', time.localtime(int(time.time()*1000) / 1000))
    return res_
