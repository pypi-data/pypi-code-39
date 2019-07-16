#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Project      : tql-CLI.
# @File         : cli
# @Time         : 2019-07-11 15:34
# @Author       : yuanjie
# @Email        : yuanjie@xiaomi.com
# @Software     : PyCharm
# @Description  : 


import fire
from .clis.send_mail import send_mail
from .clis.spark_submit import spark_submit as spark


def main():
    fire.Fire()


if __name__ == '__main__':
    fire.Fire()
