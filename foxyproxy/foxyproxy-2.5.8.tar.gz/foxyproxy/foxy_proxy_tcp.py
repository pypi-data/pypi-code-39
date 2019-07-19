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
import future
import traceback
from queue import Empty

from foxyproxy.client_thread import ClientThread
from foxyproxy.csp import BaseCryptoService, BaseCryptoServiceStorage, ClientResult, TokenRecord

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
        locks = {}
        general_lock = multiprocessing.Lock()
        # now keep talking with the client

        while True and ((stop_event is None) or (not stop_event.is_set())):
            # wait to accept a connection - blocking call
            try:
                # no budget for new connections? -> stop and wait for some threads to complete
                while available_threads < 1:
                    result = request_results.get()  # type: ClientResult
                    if result is not None:
                        if result.type == 1:
                            # update the state of the smartcard
                            for each in signer.storage.cert_names:  # type: TokenRecord
                                if result.reader == each.reader:
                                    each.pin = result.pin
                                    each.file_id = result.file_id
                        elif result.type == 2:
                            signer.storage.last_enum_reader = result.last_enum_id


                    logging.debug('Client thread released budget - case 0 ')
                    available_threads += 1

                conn = None
                while conn is None:
                    try:
                        soc.settimeout(0.5)  # we need to interrupt waiting
                        conn, addr = soc.accept()
                    except socket.timeout:
                        # if we run out of the thread budget, get some back
                        try:
                            while True:
                                # this throws exception when the queue is empty
                                result = request_results.get(block=False)  # type: ClientResult
                                if result is not None:
                                    if result.type == 1:
                                        # update the state of the smartcard
                                        for each in signer.storage.cert_names:  # type: TokenRecord
                                            if result.reader == each.reader:
                                                each.pin = result.pin
                                                each.file_id = result.file_id
                                available_threads += 1
                                logging.debug('Client thread released budget - case 1')
                        except Empty:
                            pass

                available_threads -= 1
                # noinspection PyUnboundLocalVariable
                ip, port = str(addr[0]), str(addr[1])
                logging.debug('A new connection from {0}:{1}, remaining budget is {2}'
                              .format(ip, port, available_threads))

                # signer.process_updates()
                # start new thread takes with arguments
                new_client = ClientThread("tcp", conn, signer, request_results)
                new_client.name = "tcp connection"
                reader_name = new_client.read_request()  # we get a reader here, or possibly "name" from certificate
                new_lock = None
                # we need to lock the smartcard so that it is not accessed twice
                if reader_name in signer.storage.certificates:
                    if reader_name not in locks:
                        locks[reader_name] = multiprocessing.Lock()  # we create new locks as cards are accessed
                    new_lock = locks[reader_name]
                else:
                    # it may be a name -> let's try to get
                    # only of the first commands is SIGN or CHAIN
                    set_new_name = False
                    if len(new_client.req_commands) > 0:
                        if new_client.req_commands[0]['name'] in ['CHAIN', 'SIGN']:
                            _name = signer.get_token(reader_name)  # tye: List
                            if len(_name) == 1:
                                _reader = _name[0]  # type: TokenRecord
                                new_client.real_reader_name = _reader.reader
                                new_client.real_reader = _reader
                                set_new_name = True
                                if reader_name not in locks:
                                    locks[reader_name] = multiprocessing.Lock()  # we create new locks as cards are accessed
                                new_lock = locks[reader_name]
                    if not set_new_name:
                        new_client.real_reader_name = None  # make sure it's None
                if new_lock is None:
                    new_lock = general_lock

                new_client.set_lock(new_lock)
                new_client.start()

                # new_client.join()  # commenting this out -> multi-threaded processing
            except BaseException as ex:
                tb = "; ".join(traceback.format_exc(3).splitlines())
                logging.warning("Exception in accept: {0} ({1}), stopping event: {2}"
                                .format(str(ex), tb, stop_event.is_set()))

        # soc.close()  #  unreachable
