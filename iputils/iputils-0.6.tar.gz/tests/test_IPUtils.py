#!/usr/bin/env python
# -*- coding: utf-8 -*-
#
# date:        2019/6/6
# author:      he.zhiming
#

from __future__ import (absolute_import, unicode_literals)

import pytest
from ipaddress import *

from iputils import *
import iputils


@pytest.mark.parametrize(
    ['ip', 'expected'],
    [
        ['1', False],
        [2, True],
        ['127..0.0.1', False],
        ['256.0.0.1', False],
        ['127.0.0.1.1', False],
        ['127.0.0.1', True],
        ['199.201.89.100/33', False],

        ['0.0.0.0', True],
        ['255.255.255.255', True],
        ['199.201.89.100/22', True],

        ['2001::0::1/64', False],
        ['2001::1/64', True]
    ]
)
def test_is_valid(ip, expected):
    assert IPUtils.is_valid(ip) is expected


@pytest.mark.parametrize(
    ['ip', 'expected'],
    [
        ['190.90.90.90/22', True],
        ['2001::1/64', False]
    ]
)
def test_is_ipv4(ip, expected):
    assert IPUtils.is_ipv4(ip) is expected


@pytest.mark.parametrize(
    ['ip', 'expected'],
    [
        ['190.90.90.90/22', False],
        ['2001::1/64', True]
    ]
)
def test_is_ipv6(ip, expected):
    assert IPUtils.is_ipv6(ip) is expected


@pytest.mark.parametrize(
    ['ip', 'expected'],
    [
        ['127.1.2.100/24', '127.1.2.0/24'],
        ['2001::1/64', '2001::/64']
    ]
)
def test_get_network_addr(ip, expected):
    assert IPUtils.get_network_addr(ip) == expected


@pytest.mark.parametrize(
    ['ip', 'expected'],
    [
        ['127.1.1.100/24', '127.1.1.255'],
        ['2001::1/127', '2001::1']
    ]
)
def test_get_broadcast_addr(ip, expected):
    assert IPUtils.get_broadcast_addr(ip) == expected


@pytest.mark.parametrize(
    ['ip', 'e'],
    [
        ['127.0.0.1/16', False],
        ['127.0.0.0/16', True],

        ['2001::1/64', False],
        ['2001::/64', True]
    ]
)
def test_is_network(ip, e):
    assert IPUtils.is_network(ip) is e


@pytest.mark.parametrize(
    ['ip', 'e'],
    [
        ['199.201.90.100/255.255.252.0', '199.201.90.100/22'],
        ['2001::1/64', '2001::1/64']
    ]
)
def test_with_prefix(ip, e):
    assert IPUtils.with_prefix(ip) == e


@pytest.mark.parametrize(
    ['ip', 'e'],
    [
        ['199.201.90.100/22', '199.201.90.100/255.255.252.0'],
        ['2001::1/64', '2001::1/ffff:ffff:ffff:ffff::']
    ]
)
def test_with_netmask(ip, e):
    assert IPUtils.with_netmask(ip) == e


@pytest.mark.parametrize(
    ['ip', 'e'],
    [
        ['127.0.0.1/24', '127.0.0.0/8'],
        ['199.201.89.0/22', None],
        ['4001::1/64', '4000::/3'],
        ['2001::1/64', None]
    ]
)
def test_get_belong_special_network(ip, e):
    assert IPUtils.get_belong_special_network(ip) == e


@pytest.mark.parametrize(
    ['ipobj', 'e'],
    [
        [IPv4Address("192.10.1.1"), True],
        [ip_interface('199.201.89.100/22'), True],
        [ip_network('199.201.88.0/22'), False]
    ]
)
def test__is_ip_address(ipobj, e):
    assert iputils._is_ip_address(ipobj) is e


@pytest.mark.parametrize(
    ['ips', 'expected'],
    [
        [['199.201.90.100/255.255.252.0', '199.201.90.100/22'], True]
    ]
)
def test_is_ips_equal(ips, expected):
    assert IPUtils.is_ips_equal(*ips) is expected


def test_get_special_networks():
    print(IPUtils.get_special_networks(version=4))
    print(IPUtils.get_special_networks(version=6))

    print(sum(
        IPUtils.get_ip_amount(item)
        for item in IPUtils.get_special_networks(version=6)
    ) - (2 ** 128))
    print(sum(
        IPUtils.get_ip_amount(item)
        for item in IPUtils.get_special_networks(version=4)
    ) - (2 ** 32))


@pytest.mark.parametrize(
    ['ip1', 'ip2'],
    [
        ['', None],
        [None, None],
        [None, ''],
        ['2001::/64', '%%']
    ]
)
def test_test_is_same_ip_version_exc(ip1, ip2):
    with pytest.raises(IPException, match=r'invalid ip .+?'):
        IPUtils.is_same_ip_version(ip1, ip2)


@pytest.mark.parametrize(
    ['ip1', 'ip2', 'expected'],
    [
        ['199.201.89.100', '2001::1/64', False],
        ['199.201.89.100', '199.201.89.11/255.255.255.0', True]

    ]
)
def test_is_same_ip_version(ip1, ip2, expected):
    assert IPUtils.is_same_ip_version(ip1, ip2) is expected


@pytest.mark.parametrize(
    ['ip1', 'ip2', ],
    [
        [None, None],
        [None, ''],
        ['', None],
        ['', ''],
        ['2001::/64', '$$']
    ]
)
def test_is_ip_in_network_exc(ip1, ip2):
    with pytest.raises(IPException, match=r'invalid ip .+?') as exc:
        IPUtils.is_ip_in_network(ip1, ip2)


@pytest.mark.parametrize(
    ['ip', 'ip2', 'expected'],
    [
        ['2001::1/64', '2001::ffff/64', True]
    ]
)
def test_is_ip_in_network(ip, ip2, expected):
    assert IPUtils.is_ip_in_network(ip, ip2) is expected


@pytest.mark.parametrize(
    ['ip1', 'ip2', 'exchange', 'expected'],
    [
        ['199.201.90.100/8', '199.201.89.11/24', True, True],
        ['199.201.90.100/8', '199.201.89.11/24', False, False]
    ]
)
def test_is_subnet(ip1, ip2, exchange, expected):
    assert IPUtils.is_subnet(ip1, ip2, exchange=exchange) is expected


