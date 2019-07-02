# coding=utf-8
import vlan_schema
import vlan_ip_schema
import vlan_update_schema
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import json
import traceback
from pyangbind.lib.xpathhelper import YANGPathHelper
import vlan_validate
import bgp_network_validate
import portChannel_validate


def start_check(type, action, target, current_config, options=None):
    msg = "ok"
    module = type + "_check"
    msg = globals().get(module)(action, target, current_config)
    return msg


def vlan_check(action, target, current_config):

    if action == "add":
        ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
        msg = vlan_validate.check_add_vlan_ip(target, current_config)
        return msg


    if action == "new":
        try:
            return vlan_validate.check_new_vlan(target, current_config)

        except Exception, e:
            return "配置未通过yang model检测:" + str(e)


    if action == "update":
        try:
            msg = vlan_validate.check_update_vlan(target, current_config)
            return msg
        except Exception, e:
            return "配置未通过yang model监测:"+ str(e)

    if action == "remove":
        try:
            msg = vlan_validate.check_vlan_remove_ip(target, current_config)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + str(e)


def portChannel_check(action, target, current_config):
    if action == "add_vlan":
        try:
        ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
            msg = portChannel_validate.check_add_vlan(target, current_config)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + str(e)


    if action == "remove_vlan":
        try:
            msg = portChannel_validate.check_remove_vlan(target, current_config)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + str(e)

def bgp_network_check(action, target, current_config):
    if action == "add":
        try:
            ## 如果是增则对 先检查整体添加完后是否符合yang model 然后对所有相关的key进行逐一增加检查
            msg = bgp_network_validate.check_bgp_network_add_ip(target, current_config)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + str(e)

    if action == "remove":
        try:
            msg = bgp_network_validate.check_bgp_network_remove_ip(target, current_config)
            return msg
        except Exception, e:
            print traceback.format_exc(e)
            return "配置未通过yang model检测:" + str(e)




if __name__ == "__main__":
    target = {
        "Vlan701": {
            "vrf": "global",
            "description": "default gateway",
            "adminStatus": "up",
            "aclIn": "AL01",
            "aclOut": "AL02",
            "mtu": "9280",
            "arpProxy": "enable",
            "dhcpRelaySrcIP": "12.162.231.2",
            "dhcpSever": [
                "100.0.0.2"
            ],
            "ndpProxy": "enable"
        }
    }

    current_config = {
        "VLAN":target
    }

    # current = {"VLAN": {
    #     "VLAN10": {
    #         "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
    #         "ipv6Address": ["fe00::4/64", "fe00::3/64"]
    #     }
    # }
    # }
    # # msg = check_new_vlan(target, current)
    msg = start_check("vlan", "new", target, current_config)
    print msg
