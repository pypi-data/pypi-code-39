#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:        2019/6/6
# author:      he.zhiming
#

from __future__ import (absolute_import, unicode_literals)

import ipaddress
from ipaddress import _IPv4Constants, _IPv6Constants
from ipaddress import ip_interface, ip_network

_SPECIAL_NETWORKS_IPV4 = frozenset((
    _IPv4Constants._loopback_network,
    _IPv4Constants._multicast_network,
    _IPv4Constants._reserved_network,
    _IPv4Constants._unspecified_address
))
_SPECIAL_NETWORKS_IPV6 = frozenset(
    [_IPv6Constants._multicast_network,
     _IPv6Constants._sitelocal_network] + _IPv6Constants._reserved_networks
)


def _is_ip_address(ipobj):
    return isinstance(ipobj, (ipaddress.IPv4Address, ipaddress.IPv6Address))


def _is_ip_network(ipobj):
    return isinstance(ipobj, (ipaddress.IPv4Network, ipaddress.IPv6Network))


class IPException(Exception):
    """异常类"""
    pass


class IPUtils:
    @classmethod
    def get_special_networks(cls, version: int = 4):
        """获取特殊网络的列表

        :param version: IP的版本
        :return: 特殊网络的IP列表
        :rtype: list[str]
        """
        if version == 4:
            return [str(item) for item in _SPECIAL_NETWORKS_IPV4]
        if version == 6:
            return [str(item) for item in _SPECIAL_NETWORKS_IPV6]

    @classmethod
    def is_special_ip(cls, ip, *,
                      check_link_local=True,
                      check_multicast=True,
                      check_loopback=True,
                      check_reserved=True,
                      check_site_local=True,
                      check_unspecified=True):
        """是否为特殊IP

        :param ip:
        :return:
        """
        cls.check_ips_valid(ip)

        obj = ip_interface(ip)

        is_special = True
        if check_loopback:
            is_special = is_special or obj.is_loopback
        if check_link_local:
            is_special = is_special or obj.is_link_local
        if check_multicast:
            is_special = is_special or obj.is_multicast
        if check_reserved:
            is_special = is_special or obj.is_reserved
        if check_site_local:
            is_special = is_special or obj.is_site_local
        if check_unspecified:
            is_special = is_special or obj.is_unspecified

        return is_special

    @classmethod
    def is_useable_ip(cls, ip, check_reserved=True):
        return cls.is_valid(ip) and (not cls.is_special_ip(ip, check_reserved=check_reserved))

    @classmethod
    def get_ip_amount(cls, network: str, strict=False):
        """获取一个网络内的IP数目

        :param network: 网段地址
        :param strict: 是否严格模式
        :return: IP数量
        :rtype: int
        """
        net = ip_network(network, strict=strict)

        return net.num_addresses

    @classmethod
    def is_valid(cls, ip: str) -> bool:
        """IP是否合法

        :param ip: IP地址(4/6)
        :return:
        """
        try:
            ip_interface(ip)
            return True
        except ValueError:
            return False

    @classmethod
    def is_ipv4(cls, ip):
        """是否为IPv4地址

        :param ip:
        :return:
        """
        return ip_interface(ip).version == 4

    @classmethod
    def is_ipv6(cls, ip):
        """是否为IPv6地址

        :param ip:
        :return:
        """
        return ip_interface(ip).version == 6

    @classmethod
    @classmethod
    def is_network(cls, ip, strict=True):
        """是否是一个网段

        :param ip:
        :param strict: 是否为严格模式. 建议使用True
        :return:
        """
        try:
            ip_network(ip, strict=strict)
            return True
        except ValueError:
            return False

    @classmethod
    def get_network_addr(cls, ip):
        """获取网段地址

        :param ip: 某IP地址
        :return:
        """
        return str(ip_interface(ip).network)

    @classmethod
    def get_broadcast_addr(cls, ip):
        """获取广播地址

        :param ip: 某IP地址
        :return:
        """
        n = ip_interface(ip).network

        return str(n.broadcast_address)

    @classmethod
    def with_prefix(cls, ip):
        """转化成前缀格式的IP

        :param ip: 子网掩码格式的IP
        :return:
        """
        return ip_interface(ip).with_prefixlen

    @classmethod
    def with_netmask(cls, ip):
        """转化成子网掩码格式的IP

        :param ip: 前缀形式的IP
        :return:
        """
        return ip_interface(ip).with_netmask

    @classmethod
    def get_belong_special_network(cls, ip):
        """获取属于哪个特殊网络

        :param ip:
        :return:
        """
        ipint = cls.ip_to_int(ip)

        if cls.is_ipv4(ip):
            for net in _SPECIAL_NETWORKS_IPV4:
                if _is_ip_address(net):
                    if ipint == int(net):
                        return str(net)
                if cls._is_in_network(ip, net):
                    return str(net)

        if cls.is_ipv6(ip):
            for net in _SPECIAL_NETWORKS_IPV6:
                if _is_ip_address(net):
                    if ipint == int(net):
                        return str(net)
                if cls._is_in_network(ip, net):
                    return str(net)

        return None

    @classmethod
    def ip_to_int(cls, ip):
        return int(ip_interface(ip))

    @classmethod
    def int_to_ip(cls, number, version=4):
        if version == 4:
            return str(ipaddress.IPv4Interface(number).ip)

        if version == 6:
            return str(ipaddress.IPv6Interface(number).ip)

        raise IPException(f'not support version: {version}')

    @classmethod
    def is_in_network(cls, ip, network, strict=True):
        """某IP是否在某网络内

        :param ip:
        :param network:
        :param strict: 严格的网络地址
        :return:
        """
        return cls._is_in_network(ip, ipaddress.ip_network(network, strict=strict))

    @classmethod
    def is_ips_equal(cls, *ips):
        """多个IP是否相等

        :param ips:
        :return:
        """
        return len({cls.ip_to_int(ip) for ip in ips}) == 1

    @classmethod
    def _is_in_network(cls, ip, network_obj):
        ipint = cls.ip_to_int(ip)

        if _is_ip_address(network_obj):
            return ipint == int(network_obj)

        return int(network_obj[0]) <= ipint <= int(network_obj[-1])

    @classmethod
    def is_same_ip_version(cls, ip1, ip2):
        if not (cls.is_valid(ip1) and cls.is_valid(ip2)):
            raise IPException(f'invalid ip input {ip1} {ip2}')

        return ip_interface(ip1).version == ip_interface(ip2).version

    @classmethod
    def is_ip_in_network(cls, ip1, network_ip, *, strict=False):
        if not (cls.is_valid(ip1) and cls.is_valid(network_ip)):
            raise IPException(f'invalid ip input {ip1} {network_ip}')

        net = ip_network(network_ip, strict=strict)

        return cls._is_in_network(ip1, net)

    @classmethod
    def is_subnet(cls, ip1, ip2, *, exchange=True):
        cls.check_ips_valid(ip1, ip2)

        net1 = ip_network(ip1, strict=False)
        net2 = ip_network(ip2, strict=False)

        is_subnet = net1.subnet_of(net2)
        if exchange:
            is_subnet = is_subnet or net2.subnet_of(net1)

        return is_subnet

    @classmethod
    def check_ip_valid(cls, ip):
        if not cls.is_valid(ip):
            raise IPException(f'invalid ip input {ip}')

    @classmethod
    def check_ips_valid(cls, *ips):
        for ip in ips:
            cls.check_ip_valid(ip)
