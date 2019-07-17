# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zhanglanhui
homepage recommender:ffm
"""
import os


def file_repalce(source, dest):
    if os.path.exists(dest):
        os.remove(dest)
        os.rename(source, dest)
    else:
        os.rename(source, dest)


def get_updir_path():
    return os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def get_upupdir_path():
    return os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))


def get_dir_path():
    return os.path.abspath(os.path.dirname(__file__))
