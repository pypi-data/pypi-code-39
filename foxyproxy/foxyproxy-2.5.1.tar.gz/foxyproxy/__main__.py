# !/usr/bin/env python
# -*- coding: utf-8 -*-

"""
***
Module: foxyproxy - CloudFoxy proxy - TCP proxy for flexible access to CloudFoxy RESTful API
***

# Copyright (C) Smart Arcs Ltd registered in the United Kingdom.
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# This file is provided under a license as specified in the "LICENSE" file, which is part
# of this software package.
#
# Written by Smart Arcs <support@smartarchitects.co.uk>, August 2018
"""
import multiprocessing
import signal
import sys
# import socket
# import threading
# import time

# import logbook
# import logging
import getopt
import os

from foxyproxy.beacon_thread import BeaconThread
from foxyproxy.foxy_proxy_tcp import FoxyProxyTCP
from foxyproxy.foxy_proxy_rest import FoxyProxyREST
from foxyproxy.csp import Register
from foxyproxy.queue_handler import QueueHandler
# from log_dispatcher import LogDispatcher
# from foxyproxy.logger import TCPHandler
import logging

__author__ = "Smart Arcs"
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Beta'

proxy_version = '2.5.1'

logger = logging.getLogger()
# logging.basicConfig(level=logging.DEBUG)
logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
ch = QueueHandler()
fmt = logging.Formatter('%(asctime)s - Q - %(name)s - %(levelname)s - %(message)s')
ch.setFormatter(fmt)
ch.setLevel(logging.INFO)
logger.addHandler(ch)
# coloredlogs.install(level='INFO', logger=logger)
# logging.basicConfig(level=logging.DEBUG)


main_stop = multiprocessing.Event()


def print_help():
    """
    A simple help printing
    """
    print("foxyproxy, version %s. (c) Smart Arcs Ltd. Visit https://gitlab.com/cloudfoxy .\n\n"
          "The proxy accepts the following parameters:" % proxy_version)
    print("  -h, --help - this help, if present it will stop the process\n")
    print("  -l  <DEBUG|ERROR|WARNING|INFO> - minimum level to log, default is INFO")
    print("  -r, --register - will attempt to create certification request(s)\n")
    print("  -p <port>, --port <port> - port where the proxy listens, 4001 if not set\n")
    print("  -p2 <port>, --port2 <port> - port where proxy's RESTful and WS server listens, 4443 if not set\n")
    print("  -k <path>, --keys <path> - location of keys for downstream RESTfull HTTPS (folder must contain files ")
    print("        'privkey.pem' and 'fullchain.pem' files in LetsEncrypt format; if not present, HTTP only\n")
    print("  -s http(s)://<url:port>|file://<path>|python://dummy> - address of the upstream server, e.g., ")
    print("        FoxyRest - http://upstream.cloudfoxy.com:8081 ; 'python://' will use an internal simulator\n")
    print("  -c <signer>, --signer <signer> - identification of the signature provider; currently supported are "
          "\"ICA\", \"PGP\"\n")
    print("  -t <token>, --token <token> - authorization token / API key for the signing API")


# def setup_logging(level=logbook.DEBUG, true_socket=False):
#     """
#
#     :param level:
#     :param true_socket:
#     :return:
#     """
#
#     if true_socket:
#         local_sock = socket.gethostbyname("localhost")
#         port = 44444
#         _handler = TCPHandler(None, flush_threshold=1, flush_time=0, ip=local_sock, port=port,
#                               extra_fields={}, level=level)
#     else:
#         sock_file = os.path.join('/etc/foxyproxy/logbook.sock')
#         _handler = TCPHandler(sock_file, flush_threshold=1, flush_time=0,
#                               extra_fields={}, level=level)
#     # noinspection PyBroadException
#     try:
#         _handler.pop_application()
#     except BaseException:
#         pass
#     _handler.push_application()


# noinspection PyUnusedLocal
def signal_handler(sig, frame):
    """
    Signal handler
    :param sig:
    :param frame:
    :return:
    """
    global main_stop

    main_stop.set()
    raise SystemExit('Terminating FoxyProxy')


def main():
    """
    Main entry function
    """

    global main_stop

    signal.signal(signal.SIGINT, signal_handler)

    # noinspection PyUnusedLocal
    foxyproxy_port = None
    upstream_server = None
    token = None
    register = False
    key_folder = None  # if none, RESTful will be HTTP only
    signer_name = 'ica'
    foxyproxy_port = 0
    foxyproxy_port2 = 0
    # log_level = logbook.DEBUG
    log_level = logging.INFO

    if len(sys.argv) > 1:
        try:
            opts, args = getopt.getopt(sys.argv[1:], 'hrp:s:t:c:',
                                       ['help', 'register', 'port=', 'server=', 'signer=', 'token='])
        except getopt.GetoptError:
            # print help information and exit:
            print_help()
            print("You provided %s" % ' '.join(sys.argv[1:]))
            sys.exit(2)

        for o, a in opts:
            if o in ('-h', '--help'):
                print_help()
                exit(0)
            else:
                if o in ('-r', '--register'):
                    register = True
                if o in ('-p', '--port'):
                    if a.isdigit():
                        foxyproxy_port = int(a)
                    else:
                        print("Invalid value of the port, it has to be a number")
                if o in ('-l', '--level'):
                    _a = ("%s" % a).lower()
                    if _a == 'debug':
                        log_level = logging.DEBUG
                    elif _a == 'info':
                        log_level = logging.INFO
                    elif _a == 'error':
                        log_level = logging.ERROR
                    elif _a == 'warning':
                        log_level = logging.WARNING

                if o in ('-p2', '--port2'):
                    if a.isdigit():
                        foxyproxy_port2 = int(a)
                    else:
                        print("Invalid value of the port2, it has to be a number")
                if o in ('-s', '--server'):
                    upstream_server = a.strip()
                if o in ('-c', '--signer'):
                    signer_name = a.strip().lower()
                if o in ('-t', '--token'):
                    token = a.strip()
                if o in ('-k', '-keys'):
                    key_folder = a.strip()

    # alternative logbook logging
    # log_dispatcher_thread = LogDispatcher(logger_stop_event, ip="127.0.0.1")
    # log_dispatcher_thread.name = "LogDispatcher"
    # log_dispatcher_thread.start()

    # setup_logging(log_level, true_socket=True)  # alternative logbook logging
    logger.setLevel(log_level)

    upstream_test = upstream_server.lower().split('://')
    if ((len(upstream_test) < 2) or ((upstream_test[0] != 'file') and (upstream_test[0] != 'http')
                                     and (upstream_test[0] != 'https'))) and (upstream_test[0] != 'python'):
        print("Upstream signer must start with 'file://' or 'http://' or 'https://' or 'python")
        exit(-1)

    if (foxyproxy_port == foxyproxy_port2) and foxyproxy_port > 0:
        print("port and port2 must be different")
        exit(-1)
    if upstream_test[0] == 'file':
        # let's try to open the file
        file_path = upstream_test[1]
        if not os.path.isfile(file_path):
            print("Can't open the local signer %s" % file_path)
            exit(-1)
        if not os.access(file_path, os.R_OK):
            print("The local signer %s is not readable" % file_path)
            exit(-1)

    # create a manager to share data between processes and to allow update - e.g., last PIN used
    # process_manager = Manager()  # throws errors on connections probably due to gevent present in the project

    cmd_line = dict(upstream=upstream_server, signer=signer_name, token=token, register=register)

    # create an instance of the signing service according to the CLI parameters, default is:
    #  'ica', http://localhost:8081, token='b'
    signer = Register.get_service(cmd_line)

    # let's start checking the status of the upstream server - it works even when the upstream is just a
    # local command
    new_beacon = BeaconThread(signer, stop_event=main_stop)
    new_beacon.name = "BeaconThread"
    new_beacon.start()

    if not register:
        # and we finally start the proxy itself to accept client requests
        # first RESTful API

        restful = FoxyProxyREST(signer, downstream_port=foxyproxy_port, key_folder=key_folder)
        restful.name = "RESTAPI"
        restful.start()

        # and then TCP server
        FoxyProxyTCP.start_server(downstream_port=foxyproxy_port, signer=signer, stop_event=main_stop)


if __name__ == '__main__':
    os.setpgrp()  # create new process group, become its leader
    try:
        main()
    finally:
        os.killpg(0, signal.SIGKILL)  # kill all processes in my group
