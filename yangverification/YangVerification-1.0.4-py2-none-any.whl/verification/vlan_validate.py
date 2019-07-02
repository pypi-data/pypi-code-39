# coding=utf-8
from pyangbind.lib.xpathhelper import YANGPathHelper
import pyangbind.lib.pybindJSON as pybindJSON
from pyangbind.lib.serialise import pybindJSONDecoder
import traceback
import json
import vlan_schema
import vlan_ip_schema
import vlan_update_schema
from common import get_current_config


def get_current_vlan(current_config, ph):
    ### 这里预留获取逻辑 直接在task上实现或者如果校验是个模板的话则调用get模板来实现
    ### 暂时只能用北向api来实现

    try:
        result = {
            "VLAN": current_config.get("VLAN")
        }
        current_vlan = pybindJSON.loads(result, vlan_schema, "vlan_schema", path_helper=ph)
    except Exception, e:
        raise Exception("设备上vlan配置未通过yang model 校验" + str(e))
    return current_vlan


def check_add_vlan_ip(target, current_config):
    ## 新增只允许新增ipAddress

    ph = YANGPathHelper()
    try:
        # current_config = get_current_config(hostname)

        ## 返回的是一个Json对象
        current_vlan = get_current_vlan(current_config, ph)

    except Exception, e:
        print traceback.format_exc(e)
        return str(e)

    try:
        vlan_ip_target = {
            "VLAN_IP": target
        }
        additional = pybindJSON.loads(vlan_ip_target, vlan_ip_schema, "vlan_ip_schema", path_helper=ph)
    except Exception, e:
        print traceback.format_exc(e)
        return "配置未通过yang model检测:" + str(e)

    ip_types = ["ipv4Address", "ipv6Address", "ipv6Linklocal"]
    try:
        addtional = target
        base = current_config["VLAN"]
        for k in addtional.keys():
            vlan_base_ipAddress = base[k]
            addtional_ipAddress = addtional[k]
            for ip_type in ip_types:
                if addtional_ipAddress.get(ip_type, []) and vlan_base_ipAddress.get(ip_type, []):
                    for ip in addtional_ipAddress[ip_type]:
                        if ip in vlan_base_ipAddress[ip_type]:
                            return "存在重复ip" + ip
                    vlan_base_ipAddress[ip_type].extend(addtional_ipAddress[ip_type])
                elif not addtional_ipAddress.get(ip_type, []):
                    continue
                else:
                    vlan_base_ipAddress[ip_type] = addtional_ipAddress[ip_type]

        current = {
            "VLAN": current_config.get("VLAN")
        }
        pybindJSON.loads(current, vlan_schema, "vlan_schema", path_helper=YANGPathHelper())
        return "ok"
    except Exception, e:
        print traceback.format_exc(e)
        return "yang model转换失败,请检查配置" + str(e)


def check_new_vlan(target, current_config):
    ph = YANGPathHelper()
    try:
        # current_config = get_current_config(hostname)

        ## 返回的是一个Pyang对象
        current_vlan = get_current_vlan(current_config, ph)
    except Exception, e:
        return str(e)

    current = json.loads(pybindJSON.dumps(current_vlan))
    try:
        current_vlans = current.get("VLAN")
        for vlan in target.keys():
            if current_vlans.has_key(vlan):
                return "配置中新建vlan和交换机上已有vlan重复"
            adminStatus = target[vlan].get("adminStatus", "")
            if not adminStatus == "up":
                return "配置文件校验未通过,新建vlan，adminstatus 必须为up"

        merge_dict = {"VLAN": dict(current["VLAN"], **dict(target))}
        print merge_dict
        after = pybindJSON.loads(merge_dict, vlan_schema, "vlan_schema", path_helper=ph)
        print pybindJSON.dumps(after)
        return "ok"
    except Exception, e:
        print traceback.format_exc(e)
        return "新增配置后yang model检查失败" + str(e)


def check_vlan_remove_ip(target, current_config):
    ## 这里有一个坑 pathHelper必须用同一个对象才生效
    ph = YANGPathHelper()
    try:
        # current_config = get_current_config(hostname)

        ## 返回的是一个Pyang对象
        current_vlan = get_current_vlan(current_config, ph)
    except Exception, e:
        return str(e)

    try:
        vlan_ip_target = {
            "VLAN_IP": target
        }
        additional = pybindJSON.loads(vlan_ip_target, vlan_ip_schema, "vlan_ip_schema", path_helper=ph)
    except Exception, e:
        print traceback.format_exc(e)
        return "配置未通过yang model检测:" + str(e)

    return "ok"


def check_update_vlan(target, current_config):
    ph = YANGPathHelper()
    try:

        ## 返回的是一个Json对象
        current_vlan = get_current_vlan(current_config, ph)
    except Exception, e:
        return str(e)
    try:
        vlan_target = {
            "VLAN_UPDATE": target
        }
        additional = pybindJSON.loads(vlan_target, vlan_update_schema, "vlan_update_schema", path_helper=ph)
    except Exception, e:
        return "配置未通过yang model监测:" + str(e)
    return "ok"


if __name__ == "__main__":
    target = {
        "Vlan10": {
            "ipv4Address": [
                "11.161.116.183/26",
                "11.213.4.183/26",
                "11.167.65.247/26"
            ]
        }
    }
    current = {"VLAN": {
        "Vlan10": {
            "adminStatus": "up",
            "ipv4Address": [
                "11.161.116.184/26",
                "11.213.4.184/26",
                "11.167.65.248/26"
            ],
            "description": "down_stream_vlan",
            "ndpProxy": "enable",
            "arpProxy": "enable",
            "ipv6Linklocal": [

            ],
            "vrf": "global",
            "ipv6Address": [
                "fc00:2:0:200::1/56",
                "fe80::1/64",
                "fc00:2:1:27::1/64"
            ],
            "dhcpSever": [
                "10.137.75.65"
            ],
            "dhcpRelaySrcIP": "11.213.4.183"
        },
        "Vlan701": {
            "adminStatus": "up",
            "description": "default gateway",
            "ndpProxy": "enable",
            "arpProxy": "enable",
            "mtu": "9100",
            "dhcpSever": [

            ],
            "dhcpRelaySrcIP": "12.162.231.2"
        }
    }
    }

    print check_add_vlan_ip(target, current)
