#coding=utf-8
from uiautomator import device as d
import time

# print d.info

d.set_think_time(10)

d(text='徐龙').click()