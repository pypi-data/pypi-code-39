#!/usr/bin/env python
# coding=utf-8
# from __future__ import print_function
import os, sys

curPath = os.path.abspath(os.path.dirname(__file__))
rootPath = os.path.split(curPath)[0]
sys.path.append(rootPath)

def pullsubmodule():
    print("开始拉取子模块")

if __name__ ==  "__main__":
    print("这是一个可执行文件（app/入口文件）")
print("这是一个模块")