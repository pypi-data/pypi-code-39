# -*- coding: utf-8 -*-

import portChannel_schema
import portChannel_add_vlan_schema
import portChannel_remove_vlan_schema
import vlan_schema
from pyangbind.lib.xpathhelper import YANGPathHelper
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import traceback
from vlan_validate import get_current_vlan
import json
from common import get_current_config


def get_current_portChannel(current_config, ph):
    try:
        vlan = {
            "VLAN": current_config.get("VLAN")
        }
        current_vlan =  pybindJSON.loads(vlan, vlan_schema , "vlan_schema", path_helper=ph)
        result = {
            "PORTCHANNEL": current_config.get("PORTCHANNEL")
        }
        current_portChannel = pybindJSON.loads(result, portChannel_schema, "portChannel_schema", path_helper=ph)
    except Exception, e:
        raise Exception("设备上portchannel配置未通过yang model检查" + str(e))
    return result


def check_add_vlan(target, current_config):
    ph = YANGPathHelper()
    # current_config = get_current_config(hostname)

    try:
        ## 第一步校验当前配置
        current_porchannel = get_current_portChannel(current_config, ph)
        current_vlan = get_current_vlan(current_config, ph)

        params = {
            "PORTCHANNEL_VLAN": target
        }
        additional = pybindJSON.loads(params, portChannel_add_vlan_schema, "portChannel_add_vlan_schema",
                                      path_helper=ph)

        return "ok"
    except Exception, e:
        return "yang model检查失败" + str(e)


def check_remove_vlan(target, current_config):
    ph = YANGPathHelper()
    # current_config = get_current_config(hostname)

    try:
        ## 第一步校验当前配置
        current_porchannel = get_current_portChannel(current_config, ph)
        current_vlan = get_current_vlan(current_config, ph)

        params = {
            "PORTCHANNEL_VLAN": target
        }
        additional = pybindJSON.loads(params, portChannel_remove_vlan_schema, "portChannel_remove_vlan_schema",
                                      path_helper=ph)
        return "ok"
    except Exception, e:
        return "yang model检查失败" + str(e)

def simple_check(target):
    vlan = {"VLAN": {
        "Vlan701": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        },
        "Vlan702": {
            "ipv4Address": ["11.210.88.4/30", "192.168.0.4/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        }
    }
    }

    ph = YANGPathHelper()
    current_vlan = pybindJSON.loads(vlan, vlan_schema, "vlan_schema", path_helper=ph)
    pybindJSON.loads(target, portChannel_schema, "portChannel_schema", path_helper=ph)

def simple_add_check(current, target):
    ph = YANGPathHelper()
    vlan = {"VLAN": {
        "Vlan701": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        },
        "Vlan702": {
            "ipv4Address": ["11.210.88.4/30", "192.168.0.4/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        }
    }
    }
    current_vlan = pybindJSON.loads(vlan, vlan_schema, "vlan_schema", path_helper=ph)
    pybindJSON.loads(current, portChannel_schema, "portChannel_schema", path_helper=ph)
    pybindJSON.loads(target, portChannel_add_vlan_schema, "portChannel_add_vlan_schema", path_helper=ph)




if __name__ == "__main__":
    vlan = {"VLAN":{
        "VLAN701": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["fe00::4/64", "fe00::3/64"]
        }
    }
    }

    portChannel = {
        "PORTCHANNEL":{
        "PortChannel16": {
            "ipv4Address": ["11.210.88.1/30", "192.168.0.1/30"],
            "ipv6Address": ["FE00::1/64", "FE00::2/64"],
            "adminStatus": "up",
            "mtu": "9100",
            "permitVlan": {
                "Vlan701": {
                    "taggingMode": "untagged"
                }
            }
        }
    }}
    portChannel_vlan = {
        "PORTCHANNEL_VLAN":{
            "PortChannel16":{
                "VLANS":{
                    "Vlan702":{
                        "taggingMode":"untagged1"
                    }
                }
            }
        }
    }
    simple_check(portChannel)
    simple_add_check(portChannel, portChannel_vlan)
    ##测试通过


