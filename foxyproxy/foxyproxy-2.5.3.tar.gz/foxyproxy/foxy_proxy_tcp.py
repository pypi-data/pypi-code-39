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
 Written by Smart Arcs <support@smartarchitects.co.uk>, May 2018
"""
import logging
import multiprocessing
import socket
import sys
import time

from foxyproxy.client_thread import ClientThread

__author__ = "Smart Arcs"
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'


class FoxyProxyTCP(object):
    """
    Request processing for TCP requests
    """
    PROXY_PORT = 4001

    def __init__(self):
        pass

    @staticmethod
    def start_server(downstream_port, signer, stop_event=None):
        """
        we start one monitoring thread, while the main thread will start spawning TCP upstream threads
        when the monitoring thread detects restart of the RESTful upstream, it will load all certificates from connected
        smart-cards, these are needed for requests coming from jsignpdf - SIGN - where responses consist of
        a list of certificates and a result of signing.

        :param downstream_port: the port for the FoxyProxy server
        :type downstream_port: int
        :param signer: an instance of a subclass derived from BaseCryptoService
        :type signer: BaseCryptoService
        :param stop_event
        :type stop_event: multiprocessing.Event
        """

        if downstream_port is None or downstream_port == 0:
            downstream_port = FoxyProxyTCP.PROXY_PORT

        bound = False
        tries = 20
        soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        # MAC
        TCP_KEEPALIVE = 0x10
        # soc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # soc.setsockopt(socket.IPPROTO_TCP, TCP_KEEPALIVE, 20)

        # Linux
        # soc.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        # soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 1)  # after_idle_sec
        # soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 3)  # interval_sec
        # soc.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 5)  # max_fails

        logging.debug('FoxyProxy TCP listening socket created')

        while tries > 0 and not bound:
            try:
                soc.bind(('', downstream_port))
                logging.info('FoxyProxy socket bind complete. host:{0}, port:{1}'.
                             format("*", downstream_port))
                bound = True
            except socket.error as msg:
                logging.error('FoxyProxy bind failed. Error Code : %s' % str(msg))
                soc.close()
                tries -= 1
                time.sleep(5)
                soc = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        if not bound:
            logging.error("The port %d is used by another process" % downstream_port)
            sys.exit()

        # Start listening on socket
        soc.listen(128)  # default somaxconn
        logging.info('TCP API of FoxyProxy is up and running, listening on port %d' % downstream_port)

        request_results = multiprocessing.Queue()
        available_threads = 50

        # create locks for smartcards
        locks = [multiprocessing.Lock() for _ in range(120)]
        # now keep talking with the client

        while True and ((stop_event is None) or (not stop_event.is_set())):
            # wait to accept a connection - blocking call
            try:
                # if we run out of the thread budget, get some back
                while available_threads < 1:
                    request_results.get()  # we wait
                    available_threads += 1

                conn, addr = soc.accept()
                available_threads -= 1
                ip, port = str(addr[0]), str(addr[1])
                logging.debug('A new connection from {0}:{1}, remaining budget is {2}'
                              .format(ip, port, available_threads))

                # signer.process_updates()
                # start new thread takes with arguments
                new_client = ClientThread("tcp", conn, signer, request_results, locks)
                new_client.name = "tcp connection"
                new_client.read_request()

                new_client.start()
                check_results = request_results.get(block=False)
                while check_results is not None:
                    available_threads += 1
                    check_results = request_results.get(block=False)
                    logging.debug('Client thread released budget')

                # new_client.join()  # commenting this out -> multi-threaded processing
            except BaseException as ex:
                logging.warning("Exception in accept, possibly {0}, stopping event: {1}"
                                .format(str(ex), stop_event.is_set()))

        # soc.close()  #  unreachable
