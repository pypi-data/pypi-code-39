#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module:
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@keychest.net>, 2019
"""
import socket
from keychest_agent.logger import logger
import dns.resolver

__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@keychest.net'
__status__ = 'Development'


class TlsUtils(object):
    @staticmethod
    def ip_to_int(ip):
        """
        Converts IPv4 to integer.
        123.123.123.123 -> int

        :param ip:
        :return:
        """
        octets = str(ip).split('.')
        if len(octets) != 4:
            raise ValueError('Invalid IPv4 format, 4 octets required')

        res = 0
        for idx, octet in enumerate([int(x) for x in reversed(octets)]):
            res |= octet << (8 * idx)

        return res

    @staticmethod
    def is_ipv4(ip, port=0):
        # noinspection PyBroadException
        try:
            octets = str(ip).split('.')
            if len(octets) != 4:
                return False

            for idx, octet in enumerate([int(x) for x in reversed(octets)]):
                if octet > 255 or octet < 0:
                    return False

            if isinstance(port, int) and 0 <= port < 65536:
                return True
            else:
                return False
        except Exception:
            return False

    @staticmethod
    def int_to_ip(n):
        """
        Converts 32bit integer to the IP
        :param n:
        :return:
        """
        ip = [str((n >> (8 * i)) & 0xff) for i in range(0, 4)]
        return '.'.join(reversed(ip))

    @staticmethod
    def iter_ips(ip_start=None, ip_stop=None, ip_start_int=None, ip_stop_int=None):
        """
        Iterates over the IP range in the random order - not to trigger IDS while scanning.
        :param ip_start:
        :param ip_stop:
        :param ip_start_int:
        :param ip_stop_int:
        :return:
        """
        if ip_start_int is None:
            ip_start_int = TlsUtils.ip_to_int(ip_start)

        if ip_stop_int is None:
            ip_stop_int = TlsUtils.ip_to_int(ip_stop)

        if ip_stop_int < ip_start_int:
            raise ValueError('Invalid IP order, end > start')

        # Simple case - small range, generate sequence and shuffle
        lst = list(range(ip_start_int, ip_stop_int + 1))
        for cur in lst:
            yield TlsUtils.int_to_ip(cur)
        return

    @staticmethod
    def is_ip(hostname):
        """
        Returns true if the hostname is IPv4 or IPv6
        :param hostname:
        :return:
        """
        ipv4 = TlsUtils.is_valid_ipv4_address(hostname)
        if ipv4:
            return True
        return TlsUtils.is_valid_ipv6_address(hostname)

    @staticmethod
    def is_valid_ipv4_address(hostname):
        """
        Returns true if the hostname is IPv4
        :param hostname:
        :return:
        """

        return TlsUtils.is_ipv4(hostname)
        # r = r'^(?:(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])\.){3}(?:25[0-5]|2[0-4][0-9]|1[0-9][0-9]|[1-9]?[0-9])$'
        # if re.match(r, hostname):
        #     return True
        # return False

    @staticmethod
    def is_valid_ipv6_address(address):
        """
        Simple IPV6 address validation using hacky socket.inet_pton
        :param address:
        :return:
        """
        try:
            socket.inet_pton(socket.AF_INET6, address)
        except socket.error:  # not a valid address
            return False
        return True

class DNSUtils(object):

    @staticmethod
    def process_zone(zone, domain=""):
        """
        :param zone:
        :type zone: dns.zone.Zone
        :param  domain
        :type domain:  Union[str|None]
        :return:
        """
        name_map = {}
        if domain is None:
            domain = ""
        if (len(domain) > 0) and (domain[0] == '.'):
            domain  =  domain[1:]

        if zone is not None:
            try:
                # first, let's get 'A' and
                for (name, ttl, rdata) in zone.iterate_rdatas('A'):
                    try:
                        if len(domain)  > 0:
                            if name.to_text() == '@':
                                fqdn = domain
                            else:
                                fqdn = name.to_text() + "." + domain
                        else:
                            fqdn = name.to_text()

                        if fqdn in name_map:
                            name_map[fqdn].append(rdata.address)
                        else:
                            name_map[fqdn] = [rdata.address]
                    except Exception as ex:
                        logger.warning("Error parsing DNS zone data - A",
                                       name="%r" % name.to_text(), domain=domain, rdata="%r" % rdata.address,
                                       cause=str(ex))
            except Exception as ex:
                logger.error("Unexpected exception when parsing 'A' records from zone data",
                             cause=str(ex))

            try:
                # second, let's get 'AAAA' and
                for (name, ttl, rdata) in zone.iterate_rdatas('AAAA'):
                    try:
                        if len(domain)  > 0:
                            if name.to_text() == '@':
                                fqdn = domain
                            else:
                                fqdn = name.to_text() + "." + domain
                        else:
                            fqdn = name.to_text()

                        if fqdn in name_map:
                            name_map[fqdn].append(rdata.address)
                        else:
                            name_map[fqdn] = [rdata.address]
                    except Exception as ex:
                        logger.warning("Error parsing DNS zone data - AAAA",
                                       name="%r" % name.to_text(), domain=domain, rdata="%r" % rdata.address,
                                       cause=str(ex))
            except Exception as ex:
                logger.error("Unexpected exception when parsing 'AAAA' records from zone data",
                             cause=str(ex))

            # the last is CNAME
            try:
                # second, let's get 'AAAA' and
                for (name, ttl, rdata) in zone.iterate_rdatas('CNAME'):
                    try:
                        if len(domain) > 0:
                            if name.to_text() == '@':
                                fqdn = domain
                            else:
                                fqdn = name.to_text() + "." + domain
                        else:
                            fqdn = name.to_text()
                        if rdata.to_text() in name_map:
                            if fqdn not in name_map:  # duplicate CNAMEs??
                                name_map[fqdn] = []
                            # copy IP addresses to CNAME record
                            for each_a_record in name_map[rdata.to_text()]:
                                name_map[fqdn].append(each_a_record)
                        else:
                            logger.warning("CNAME doesn't have a valid A/AAAA record",
                                           name=name.to_text())
                    except Exception as ex:
                        logger.warning("Error parsing DNS zone data - CNAME",
                                       name="%r" % name.to_text(), domain=domain, rdata="%r" % rdata.address,
                                       cause=str(ex))
                pass
            except Exception as ex:
                logger.error("Unexpected exception when parsing 'CNAME' records from zone data",
                             cause=str(ex))
        else:
            logger.info("Zone processing called with undefoned zone")

        return name_map

class ControlUtils(object):
    @staticmethod
    def filter_banned(agent, name_map, connect=0):
        """

        :param agent:
        :param name_map:
        :param connect: positive will attempt to connect to IP addresses on the given port
        :return:
        """
        resolved = []
        tested_ips = {}
        _open = False
        for each_name in name_map:
            # noinspection PyBroadException
            for each_ip in name_map[each_name]:
                if not agent.is_banned(each_ip) and len(each_ip) > 0:
                    if each_ip in tested_ips:
                        if tested_ips[each_ip]:
                            resolved.append({'name': each_name, 'ip': each_ip})
                    else:
                        if connect > 0:
                            _open = False
                            # noinspection PyBroadException
                            try:
                                sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                                sock.settimeout(3)
                                result = sock.connect_ex((each_ip, 443))
                                if result == 0:
                                    _open = True
                                sock.close()
                            except:
                                pass
                        else:
                            _open = True
                        tested_ips[each_ip] = _open
                        if _open:
                            resolved.append({'name': each_name, 'ip': each_ip})
                        else:
                            resolved.append({'name': each_name, 'ip': None})

                else:
                    logger.debug("Found a banned IP address", ip=each_ip, name=each_name)
                    pass  # IP address is banned
            pass  # and of the name cycle

        return resolved
