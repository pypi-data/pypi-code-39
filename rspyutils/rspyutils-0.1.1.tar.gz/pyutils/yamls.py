# !/usr/bin/python
# -*- coding: UTF-8 -*-
"""
Created on MAY 21, 2018
@author: zhanglanhui
homepage recommender:ffm
"""
import os
import yaml


def read_from_yaml(file: str) -> dict:
    config_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), file)
    print(config_path)
    conf_dic = yaml.load(open(config_path, 'r'),
                         Loader=yaml.FullLoader)

    return conf_dic


if __name__ == "__main__":
    print(read_from_yaml("config/dev/server_config.yaml"))
