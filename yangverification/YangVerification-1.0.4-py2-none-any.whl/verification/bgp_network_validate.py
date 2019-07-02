# -*- coding: utf-8 -*-

import bgp_network_schema
import portChannel_add_vlan_schema
from pyangbind.lib.xpathhelper import YANGPathHelper
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import traceback
import json
from common import get_current_config

def get_current_bgp_network(current_config, ph):
    try:
        result = current_config.get("bgp_network")
        current_portChannel = pybindJSON.loads(result, bgp_network_schema, "bgp_network_schema", path_helper=ph)
    except Exception,e:
        raise Exception("设备上portchannel配置未通过yang model检查" + str(e))
    return result


def check_bgp_network_add_ip(target, current_config):
    ph = YANGPathHelper()
    # current_config = get_current_config(hostname)

    try:
        ## 第一步校验当前配置
        additional = pybindJSON.loads(target, bgp_network_schema, "bgp_network_schema",
                                      path_helper=ph)
        return "ok"
    except Exception, e:
        return "yang model检查失败" + str(e)

def check_bgp_network_remove_ip(target, current_config):
    ph = YANGPathHelper()
    # current_config = get_current_config(hostname)

    try:
        ## 第一步校验当前配置
        additional = pybindJSON.loads(target, bgp_network_schema, "bgp_network_schema",
                                      path_helper=ph)
        return "ok"
    except Exception, e:
        return "yang model检查失败" + str(e)

def simple_check(target):
    ph = YANGPathHelper()
    bgp_network = pybindJSON.loads(target, bgp_network_schema, "bgp_network_schema", path_helper=ph)
    print pybindJSON.dumps(bgp_network)


if __name__ == "__main__":
    bgp_network = {
    "vrfs":{
        "globals":{
            "addressFamily":{
                "ipv4Unicast":{
                    "routeImport": {
                        "network": {
                            "networkList": {
                                "10.20.30.0/24":
                                {
                                    "network": "10.20.30.0",
                                    "maskLength": "24",
                                    "policyName": "test"
                                }
                            }
                        }
                    }
                }
            }
        }
    }
}
    simple_check(bgp_network)