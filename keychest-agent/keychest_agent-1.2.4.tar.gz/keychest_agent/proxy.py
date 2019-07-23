#!/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module: This is a simple port-forward / proxy, written using only the default python
library. If you want to make a suggestion or fix something you can contact-me
at voorloop_at_gmail.com
Distributed over IDC(I Don't Care) license
***

 Copyright (C) Smart Arcs Ltd, registered in the United Kingdom.
 This file is owned exclusively by Smart Arcs Ltd.
 Unauthorized copying of this file, via any medium is strictly prohibited
 Proprietary and confidential
 Written by Dan Cvrcek <support@smartarchitects.co.uk>, May 2018
"""
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'


import socket
from select import select
import sys
import threading
import traceback

from keychest_agent.logger import logger
from keychest_agent.misc import TlsUtils

# Changing the buffer_size and delay, you can improve the speed and bandwidth.
# But when buffer get to high or delay go too down, you can broke things
buffer_size = 4096
delay = 0.0001
forward_to = ('a3.keychest.net', 443)


# A tee for TCP, similar to `socal -v`.
#
#           | server
# client ---|
#           | stdout

class TcpTee:

    def __init__(self, source, destination, job_id, send_up=None, reverse=True):
        """

        :param source:
        :type source: tuple
        :param destination:
        :type destination: tuple
        :param job_id: id of the job
        :type job_id: str
        :param send_up: data to send to the source at the very beginning
        :type send_up: bytearray
        :param reverse: optional data to send to the upstream server
        """
        self.destination = destination  # a tuple, the first item is a list of ip addresses
        self.source = source
        self.send_up = send_up
        self.reverse = reverse
        self.job_id = job_id
        self.clientsock = None
        self.last_channel = None

        # teesock - upstream socket
        if reverse:
            self.teesock = None
        else:
            self.teesock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.teesock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
            self.teesock.bind(source)
            self.teesock.listen(200)

        # Linked client/server sockets in both directions
        self.channel = {}

    def run(self):
        # if reverse -> we connect to upstream and some stuff up there

        if self.reverse:
            ips, port = self.destination
            next_address = None
            initial_done = False
            while len(ips) > 0:
                if next_address:
                    ips.pop(next_address)
                    each_ip = next_address
                else:
                    each_ip = ips.pop(0)
                self.destination = (each_ip, port)
                clientsock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                try:
                    clientsock.settimeout(5)
                    clientsock.connect(self.source)
                except Exception as ex:
                    tb = "; ".join(traceback.format_exc(3).splitlines())
                    logger.error('Could not connect to upstream server',
                                 target=self.source, cause=str(ex), traceback=tb, job=self.job_id)

                else:
                    serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                    try:
                        serversock.settimeout(5)
                        serversock.connect(self.destination)
                    except Exception as ex:
                        tb = "; ".join(traceback.format_exc(3).splitlines())
                        logger.error('Could not connect to server. Closing connection to client as well',
                                     target=self.destination, cause=str(ex), traceback=tb, job=self.job_id)
                        clientsock.close()
                    else:
                        logger.debug("Target connected", ip=self.source[0], job=self.job_id)

                        if not initial_done:
                            if self.send_up:
                                length = len(self.send_up)
                                _len = [0, 0, 0, 0]
                                _len[0] = length % 256
                                _len[1] = (length // 256) % 256
                                _len[2] = (length // (256*256)) % 256
                                _len[3] = (length // (256*256*256)) % 256
                                clientsock.sendall(bytes(_len))
                                clientsock.sendall(self.send_up)
                            else:
                                clientsock.sendall(bytes([0, 0, 0, 0]))
                            logger.debug('Upstream data sent', job=self.job_id)
                            initial_done = True

                        self.channel[clientsock] = serversock
                        self.channel[serversock] = clientsock
                        self.clientsock = clientsock

                        next_address = self.do_proxy()
                        if not next_address and (len(ips) > 0):
                            logger.error("do_proxy should return the next IP address",
                                         job=self.job_id, )
                            break
                        elif next_address in ips:
                            logger.debug("All good, we continue with the next IP address", job=self.job_id)
                            continue
                        elif next_address is None:
                            break
                        else:  # nont None and not in the list
                            logger.error("do_proxy returns a wrong IP address, not present in the list", job=self.job_id)
                            continue

        else:  # not reverse - we wait
            # noinspection PyUnusedLocal
            next_address = self.do_proxy()
            pass

        if self.teesock:
            # noinspection PyBroadException
            try:
                self.teesock.close()
            except:
                pass
        return  # end of the thread

    def do_proxy(self):
        """
        This creates one proxy "session" and terminates when it receives
        7x \x00 + Union[\x00, \x01] + 16x address with padding zeros from the client/upstream
        :return:
        """

        next_address = None
        try:
            while True:
                if self.teesock:
                    select_list = [self.teesock] + list(self.channel)
                else:
                    select_list = list(self.channel.values())
                # readable, writeable, exceptions - parameters are - inputs, outputs, inputs, timeout
                inputready, outputready, exceptready = select(select_list, [], select_list, 500)

                if not (inputready or outputready or exceptready):
                    # timeout
                    self.on_close(self.clientsock)
                    logger.debug("Timeout, no data received on any socket", job=self.job_id)
                    return None

                for s in inputready:
                    if s == self.teesock:
                        self.on_accept()
                        continue
                    data = s.recv(4096)
                    if not data:
                        self.on_close(s)  # shall we check other possible inputs? probably not needed
                        logger.debug("No data received = socket closed, exiting do_proxy",
                                     name=s.getsockname(), job=self.job_id)
                        return None
                    else:
                        _name = s.getsockname()
                        if isinstance(_name, tuple):
                            _name = _name[0]
                        logger.debug("Data received bytes", name=_name, count=len(data))

                    # check if we switched direction and the new one comes from upstream (-> we may need to terminate)
                    if s != self.last_channel:
                        self.last_channel = s
                        if s == self.clientsock and (data[:7] == bytes([0, 0, 0, 0, 0, 0, 0])):
                            # we are terminating this proxy
                            if data[7] == 0:
                                # we are getting IP4 address
                                next_address = 0
                                for i in range(4):
                                    next_address = next_address * 256 + data[8+i]
                                pass
                                logger.debug("Proxy received request to re-connect to a new address",
                                             ip=TlsUtils.int_to_ip(next_address), job=self.job_id)
                            elif data[7] == 1:
                                # we are getting IP6 address
                                next_address = 0
                                for i in range(16):
                                    next_address = next_address * 256 + data[8+i]
                                logger.error("Requested IPv6 address - this is not yet supported",
                                             job=self.job_id, ip=next_address)
                                pass
                            else:
                                # we terminate
                                next_address = None
                                pass
                            self.on_close(s)
                            logger.debug("Received request for re-connect, terminating do_proxy",
                                         job=self.job_id)
                            return next_address

                    self.on_recv(s, data)
                if len(exceptready) > 0:
                    self.on_close(self.clientsock)
                    return None
        finally:
            if self.clientsock:
                self.on_close(self.clientsock)
            return next_address

    def on_accept(self):
        clientsock, clientaddr = self.teesock.accept()
        serversock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            serversock.settimeout(5)
            serversock.connect(self.destination)
        except Exception as ex:
            tb = "; ".join(traceback.format_exc(3).splitlines())
            logger.error('Could not connect to server. Closing connection to client as well',
                         target=self.destination, cause=str(ex), traceback=tb)
            clientsock.close()
        else:
            logger.info("KeyChest server connected", name=clientaddr, job=self.job_id)
            self.channel[clientsock] = serversock
            self.channel[serversock] = clientsock
            self.clientsock = clientsock

    def on_close(self, sock):

        logger.info("Disconnected from target server", target=sock.getpeername(), job=self.job_id)
        othersock = self.channel[sock]

        sock.close()
        othersock.close()

        del self.channel[sock]
        del self.channel[othersock]
        self.clientsock = None
        self.last_channel = None

    def on_recv(self, sock, data):
        self.channel[sock].send(data)


class UdpTee:

    def __init__(self, source, destination, job_id, send_up=None, reverse=True):
        """

        :param source:
        :type source: tuple
        :param destination:
        :type destination: tuple
        :param job_id:
        :type job_id: str
        :param send_up:
        :type send_up: bytearray
        :param reverse:
        :type reverse: bool
        """
        self.destination = destination
        self.source = source
        self.send_up = send_up
        self.reverse = reverse
        self.job_id = job_id

        self.sock_src = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_dst = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock_src.bind(source)

    def run(self):
        while True:
            data, addr = self.sock_src.recvfrom(65565)
            if not data:
                logger.error('an error occured')
                break
            logger.debug('Received UDP data and forwarded', count=len(data), name=addr, job=self.job_id)
            self.sock_dst.sendto(data, self.destination)
            data, addr2 = self.sock_dst.recvfrom(65565)
            logger.debug('received UDP data', count=len(data), name=addr2, job=self.job_id)
            self.sock_src.sendto(data, addr)

        self.sock_src.close()
        self.sock_dst.close()


class AgentProxy(threading.Thread):

    def __init__(self, protocol, upstream, downstream, job_id, send_up=None, reverse=True):
        """
        This will open a new proxy thread. Any logs produced will be sent via the control channel.

        :param protocol: it must be "tcp" or "udp"
        :param upstream: a tuple (address, port) of the KeyChest server
        :type upstream: tuple
        :param downstream: a tuple (address, port) of the audit target
        :type downstream: tuple
        :param job_id: name of the job being processed
        :type job_id: str
        :param send_up: bytearray to send to the upstream (KeyChest server)
        :type send_up: bytearray
        :param reverse:  reverse proxy or not
        """
        super().__init__()
        self.reverse = reverse
        if protocol not in ['tcp', 'udp']:
            raise Exception()

        self.protocol = protocol
        self.destination = downstream
        self.upstream = upstream
        self.send_up = send_up
        self.job_id = job_id
        self.tee = None

    def run(self):
        if self.protocol not in ['tcp', 'udp']:
            logger.error("Unknown proxy protocol", name=self.protocol, job=self.job_id)
            return

        try:
            if self.protocol == 'tcp':
                port = self.destination[1]
                ips = self.destination[0]
                if isinstance(ips, str):
                    ips = [ips]
                self.tee = TcpTee(self.upstream, (ips, port), self.job_id, send_up=self.send_up,
                                  reverse=self.reverse)
            else:
                self.tee = UdpTee(self.upstream, self.destination, self.job_id, send_up=self.send_up,
                                  reverse=self.reverse)
            self.tee.run()
            logger.debug("Proxy thread finished", job=self.job_id)
        except Exception as ex:
            tb = "; ".join(traceback.format_exc(3).splitlines())
            logger.error("Proxy thread finished with exception", job=self.job_id, traceback=tb, cause=str(ex))
            pass
        finally:
            sys.exit(1)


if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-listen_port", default=11111, help="The port this process will listen on.", type=int)
    # parser.add_argument("-server_host", default="a3.keychest.net", help="The remote host to connect to.")
    # parser.add_argument("-server_port", default=443, help="The remote port to connect to.", type=int)
    parser.add_argument("-server_host", default="131.111.12.20", help="The remote host to connect to.")
    parser.add_argument("-server_port", default=53, help="The remote port to connect to.", type=int)
    args = parser.parse_args()

    #  logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

    # tee = TcpTee(int(args.listen_port), (args.server_host, int(args.server_port)))
    tee = UdpTee(("127.0.0.1", args.listen_port), (args.server_host, int(args.server_port)), "tj1")
    try:
        tee.run()
    except KeyboardInterrupt:
        logger.info("Ctrl C - Good Bye")
        sys.exit(1)
