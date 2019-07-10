# -*- coding: utf-8 -*-
# 生成所有的内网IP地址C段


def generate_ten_cidr_ip():
    """
    返回值：
    {"result":True,"data":["10.0.0.0",10.0.1.0",10.0.2.0"......],"message":"success"}
    """
    ret_data = {"result":True,"data":[],"message":""}
    ip_list = []
    # 10.x.x.x
    for i in range(0,256):
        for j in range(0,256):
            ip_str =""
            ip_str = str("10.") + str(i) + str(".") + str(j) + str(".0")
            ip_list.append(ip_str)
    """ 
    # 172.16.x.x - 172.31.x.x
    for m in range(16,32):
        for n in range(0,256):
            ip_str = ""
            ip_str = str("172.") + str(m) + str(".") + str(n) + str(".0")
            ip_list.append(ip_str)
    # 100.64.x.x – 100.127.x.x
    for j in range(64,128):
        for k in range(0,256):
            ip_str = ""
            ip_str = str("100.") + str(j) + str(".") + str(k) + str(".0")
            ip_list.append(ip_str)
    """
    ret_data["data"] = ip_list
    return ret_data


cidr_seg = "10.0.0.0"



