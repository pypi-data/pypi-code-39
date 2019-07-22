# -*- coding: utf-8 -*-
# net_support.py

import socket

def getIPAddr():
    for ip in socket.gethostbyname_ex(socket.gethostname())[2]:
        if ip.startswith("'127.'"):
            continue
        if ip.startswith("'169.'"):
            continue
        return ip
    return ''