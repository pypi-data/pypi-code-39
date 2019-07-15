from __future__ import absolute_import
from .HeadersFormatter import *

name = 'HeadersFormatter'

def main():
	code = HeadersFormatter()
	if code == 0:
		print('程序运行完成！')
	else :
		print('出现错误({})'.format(code))
