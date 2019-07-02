# -*- coding: utf-8 -*-

import requests
import json

def get_current_config(hostname):
    import requests
    url = "http://100.67.166.36:19999/apidoc/get_config?hostname=" + hostname
    res = requests.get(url)
    response = json.loads(res.content)

    if response.get("code", -1) != 0:
        raise ValueError("获取实时配置失败")
    conifg =  response.get("data")
    return conifg

if __name__ == "__main__":
    print get_current_config("11.161.62.23")