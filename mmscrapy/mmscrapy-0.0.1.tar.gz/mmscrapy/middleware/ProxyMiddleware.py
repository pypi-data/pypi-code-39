#!/usr/bin/env python
# -*- coding: utf-8 -*-
# @Time    : 2019/7/12 18:22
# @Author  : ganliang
# @File    : ProxyMiddleware.py
# @Desc    : 代理
import base64
import json
import logging
import random
import telnetlib


class ProxyMiddleware(object):
    # 动态代理 https://www.cnblogs.com/rwxwsblog/p/4575894.html
    PROXIES = [
        {'ip_port': '1.192.241.115:9999', 'user_pass': ''},
        {'ip_port': '1.192.242.5:9999', 'user_pass': ''},
        {'ip_port': '1.198.73.226:9999', 'user_pass': ''},
        {'ip_port': '42.238.85.175:9999', 'user_pass': ''},
        {'ip_port': '1.198.72.197:9999', 'user_pass': ''},
        {'ip_port': '112.95.204.30:8888', 'user_pass': ''},
        {'ip_port': '121.69.13.242:53281', 'user_pass': ''},
        {'ip_port': '114.249.116.186:9000', 'user_pass': ''},
    ]

    logger = logging.getLogger(__name__)

    def process_request(self, request, spider):
        proxy = random.choice(self.PROXIES)
        if proxy['user_pass'] is not None:
            request.meta['proxy'] = "http://%s" % proxy['ip_port']
            encoded_user_pass = base64.encodestring(proxy['user_pass'])
            request.headers['Proxy-Authorization'] = 'Basic ' + encoded_user_pass
            print "**************ProxyMiddleware have pass************" + proxy['ip_port']
        else:
            print "**************ProxyMiddleware no pass************" + proxy['ip_port']
            request.meta['proxy'] = "http://%s" % proxy['ip_port']

    def proxy_checker(self):
        """
        读取代理文件 解析代理
        :return:
        """
        active_hosts = []
        with open("proxys.json", "r") as proxy_file:
            for proxy_data in proxy_file:
                proxy_json = json.loads(proxy_data, encoding="UTF-8")
                # 获取到代理服务器的ip和端口
                if self.ckecker_host_avaliable(proxy_json.get("ip"), proxy_json.get("port")):
                    active_hosts.append(proxy_json)
        return active_hosts

    def ckecker_host_avaliable(self, ip, port):
        """
        使用telnet监测端口是否可用
        :param ip:
        :param port:
        :return:
        """
        flag = False
        server = telnetlib.Telnet()  # 创建一个Telnet对象
        try:
            server.open(ip, port=port, timeout=2)  # 利用Telnet对象的open方法进行tcp链接
            print('ip:{0}, port:{1} is open'.format(ip, port))
            flag = True
        except Exception as err:
            print('ip:{0}, port:{1} is not open'.format(ip, port))
        finally:
            server.close()
        return flag


if __name__ == "__main__":
    # ProxyMiddleware().ckecker_host_avaliable("42.121.252.58", "80")
    print ProxyMiddleware().proxy_checker()
