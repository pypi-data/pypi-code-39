#!/usr/bin/env python
# -*- coding: utf-8 -*-
#

"""
***
Module: client_thread - Implementation of the proxy request processing
***
"""

# Copyright (C) Smart Arcs Ltd, Enigma Bridge Ltd, registered in the United Kingdom.
# Unauthorized copying of this file, via any medium is strictly prohibited
#
# This file is provided under a license as specified in the "LICENSE" file, which is part
# of this software package.
#
# Written by Smart Arcs <support@smartarchitects.co.uk>, August 2018
import json
import logging
import time
import traceback
from multiprocessing import Process, Lock
# from threading import Thread
from foxyproxy.csp import ClientResult
from foxyproxy.constant import Constant
from foxyproxy.csp import BaseCryptoService
from foxyproxy.request_data import RequestData

__author__ = "Smart Arcs"
__copyright__ = 'Smart Arcs Ltd'
__email__ = 'support@smartarchitects.co.uk'
__status__ = 'Development'


logger = logging.getLogger(__name__)
# logger.setLevel(logging.INFO)
# ch = logging.StreamHandler()
# ch.setLevel(logging.INFO)
# logger.addHandler(ch)
# fh = logging.FileHandler('foxyproxy.log')
# fh.setLevel(logging.INFO)
# logger.addHandler(fh)


class ClientThread(Process):
    """
    Function for handling connections. This will be used to create threads
    """
    def __init__(self, protocol, connection, signer, queue_out):
        """
        :param protocol: a type of the connection to correctly send the response asynchronously: TCP, REST, WS
        :type protocol: str
        :param connection: the opened connection for response
        :type connection: socket object
        :param signer: reference of the signer
        :type signer: BaseCryptoService
        """
        super(ClientThread, self).__init__()
        self.connection = connection
        self.signer = signer
        self.protocol = protocol.lower()
        self.response = ""
        self.upstreamsession = self.signer.getupstreamconnection()
        self.req_commands = []
        self.req_reader = None
        self.req_password = None
        self.queue_out = queue_out
        self.lock = None  # type: Lock()
        self.sync_back = ClientResult()
        self.real_reader = None
        self.real_reader_name = None

    def read_request(self):
        """
        This will read the incoming request and identify the reader
        """
        if self.protocol == 'tcp':
            result = self._read_tcp()
        else:
            result = self._read_service()

        if result and (self.req_reader is not None):
            # we should check the Lock
            # self.signer.storage.card_locks[self.req_reader].acquire()
            pass
        if self.req_reader:
            self.real_reader_name = BaseCryptoService.decode_cf_reader(self.req_reader)
            return self.real_reader_name
        else:
            return None

    def run(self):
        """
        Thread body - selects TCP or REST processing
        :return:
        """
        logger.debug("Checking the chip's lock: {0}".format(self.req_reader))
        if self.lock is not None:
            self.lock.acquire()  # blocking by default
        logger.debug("Unlocked - starting ClientThread: {0}".format(self.req_reader))

        try:
            if self.protocol == 'tcp':
                self.run_tcp()
            else:
                self.run_service()
        finally:
            if self.lock is not None:  # type: Lock()
                self.lock.release()
                logging.debug("Lock has been released {0}".format(self.req_reader))
                pass
            else:
                logging.debug("No reader set for a downsream request")
            self.queue_out.put(self.sync_back)
            self.signer.closesession(self.upstreamsession)
        logger.debug("ClientThread finished")

    def _read_tcp(self):
        """
        Reads request from TCP connection
        :return:
        """
        more_coming = True
        self.req_commands = []
        self.req_reader = None
        while more_coming:
            # Receiving from client
            # first we read all the commands
            # noinspection PyBroadException
            try:
                data_raw = self.connection.recv(4096)
            except BaseException:
                break
            except IOError:
                break
            if len(data_raw) == 0:  # connection was closed
                break
            buffer_list = None
            try:
                # buffer_list.append(data_raw)
                if buffer_list is None:
                    buffer_list = data_raw
                else:
                    buffer_list += data_raw
            except TypeError:
                logging.error("Received data can't be converted to text")
                pass

            # data = ''.join(buffer_list)
            # noinspection PyBroadException
            try:
                data = buffer_list.decode('utf-8')
            except Exception:
                data = ""

            # data = ">Simona /111.222.123.033@07|\n>2:RESET|\n>3:APDU:1100000000|\n>4:APDU:2200000000|" \
            #        "\n>5:APDU:3300000000|"
            # data = ">K|\n>3:SIGN:0000000000000000000000000000000000000000|"
            lines = data.splitlines()
            commands = []

            for line in lines:
                # noinspection PyBroadException
                try:
                    logging.debug("Received data: %s" % line)
                    line = line.strip()  # remove white space - beginning & end
                    if (len(line) == 0) and len(self.req_commands) > 0:
                        more_coming = False
                        continue
                    if line[0] == '#':
                        # this may be in internal info
                        pass
                    elif line[0] != '>':
                        # we will ignore this line
                        continue
                    line = line[1:].strip()  # ignore the '>' and strip whitespaces
                    if line.rfind('|') < 0:
                        logging.debug("Possibly missing | at the end of the line %s " % line)
                    else:
                        line = line[:line.rfind(u"|")]
                    if not self.req_reader:
                        cmd_parts = line.split(u':')
                        # noinspection PyUnusedLocal
                        self.req_reader = cmd_parts[0]  # if '|' is not in string, it will take the whole line
                        if len(cmd_parts) > 1:
                            password = cmd_parts[1]
                    else:
                        cmd_parts = line.split(':')
                        if len(cmd_parts) == 1:
                            self.req_reader = cmd_parts[0]
                            continue

                        if len(cmd_parts) < 2 or len(cmd_parts) > 4:
                            logging.error('Invalid line %s - ignoring it' % line)
                            continue

                        item = {'id': cmd_parts[0], 'name': cmd_parts[1], 'bytes': None, 'object': None}
                        if len(cmd_parts) > 2:
                            item['bytes'] = cmd_parts[2]
                        if len(cmd_parts) > 3:
                            item['object'] = cmd_parts[3]
                        self.req_commands.append(item)
                except Exception:
                    pass

        if self.req_reader is None:
            logging.error("No reader ID sent")
            time.sleep(0.1)  # sleep little before making another receive attempt
            return False
        elif len(self.req_commands) < 1:
            logging.error("No commands to process")
            time.sleep(0.1)  # sleep little before making another receive attempt
            return False
        else:
            return True

    def run_tcp(self):
        """
        A TCP request processing method
        :return:
        """
        try:
            for command in self.req_commands:
                input_req = RequestData(self.req_reader,
                                        command['id'],
                                        command['name'],
                                        command['bytes'],
                                        command['object'],
                                        password=self.req_password)

                ########
                response_data = self.process_command(input_req)
                #########
                _temp_enum_id = self.signer.storage.last_enum_reader
                response = ">{0}{1}{2}{3}\n".format(input_req.command_id,
                                                    BaseCryptoService.CMD_SEPARATOR,
                                                    response_data,
                                                    BaseCryptoService.CMD_RESPONSE_END)

                if self.real_reader is not None:
                    self.sync_back.reader = self.real_reader.reader
                    self.sync_back.pin = self.real_reader.pin
                    self.sync_back.file_id = self.real_reader.file_id
                    self.sync_back.type = 1
                elif self.signer.storage.last_enum_reader != _temp_enum_id:
                    self.sync_back.type = 2
                    self.sync_back.last_enum_id = self.signer.storage.last_enum_reader

                self.response = response.encode("utf-8")
                logging.debug("Response %s" % response)
                self.connection.sendall(self.response)
            # break  # we close the connection after
        except Exception as ex:
            tb = traceback.format_exc()
            logging.info('Exception in serving response (1), ending thread - cause %s, traceback %s'
                         % (str(ex), tb))

        # Terminate connection for given client (if outside loop)
        # noinspection PyBroadException
        try:
            self.connection.close()
        except BaseException:
            pass
        return

    def _read_service(self):
        # infinite loop so that function do not terminate and thread do not end.
        # Receiving from client
        # first we read all the commands
        data_json = None
        try:
            data_json = self.connection

            if not data_json:  # connection was closed
                return False

            if "reader" not in data_json or (('command' not in data_json) and ('commands' not in data_json)):
                logging.debug("JSON structure is incorrect, it must have 'reader' and 'command'/'commands'")
                return False

            # JSON will have the following structure
            #  {
            #       "reader": "Simona /111.222.123.033@07",
            #       "commands": [
            #           { "nonce": "2",
            #             "line": "RESET" },
            #           { "nonce": "3",
            #             "line": "APDU:1100000000" }
            #       ],
            #       "command": {"nonce": "2",
            #                   "line": "RESET"}
            #  }

            self.req_reader = data_json['reader']

            if 'password' in data_json:  # this is not currently used
                self.req_password = data_json['password']
            else:
                self.req_password = None

            if "command" in data_json:
                command = data_json['command']

                if ("id" in command) and ("line" in command):
                    cmd_id = command['id']
                    cmd_line = command['line']
                    cmd_parts = cmd_line.split(':')
                    if len(cmd_parts) < 1 or len(cmd_parts) > 3:
                        logging.error('Invalid line %s - ignoring it' % cmd_line)
                    else:
                        item = {'id': cmd_id, 'name': cmd_parts[0], 'bytes': None, 'object': None}
                        if len(cmd_parts) > 1:
                            item['bytes'] = cmd_parts[1]
                        if len(cmd_parts) > 2:
                            item['object'] = cmd_parts[2]
                        self.req_commands.append(item)
                else:
                    logging.debug("The 'command' element has a missing 'id' or 'line'")

            if "commands" in data_json:
                for each_cmd in data_json['commands']:
                    if ("id" in each_cmd) and ("line" in each_cmd):
                        cmd_id = each_cmd['id']
                        cmd_line = each_cmd['line']
                        cmd_parts = cmd_line(':')
                        if len(cmd_parts) < 1 or len(cmd_parts) > 3:
                            logging.error('Invalid line %s - ignoring it' % cmd_line)
                        else:
                            item = {'id': cmd_id, 'name': cmd_parts[0], 'bytes': None, 'object': None}
                            if len(cmd_parts) > 1:
                                item['bytes'] = cmd_parts[1]
                            if len(cmd_parts) > 2:
                                item['object'] = cmd_parts[2]
                            self.req_commands.append(item)
                    else:
                        logging.debug("An item in 'commands' element has a missing 'id' or 'line'")

            if len(self.req_commands) == 0:
                logging.error("No commands to process")
                return False
            else:
                return True
        except Exception as ex:
            if data_json:
                data_string = json.dumps(data_json)
            else:
                data_string = ""
            logging.debug("Error reading client request - service (error: %s) %s"
                          % (str(ex), data_string))
            return False

    def run_service(self):
        """
        The main service loop
        :return:
        """
        try:
            response_json = []
            for command in self.req_commands:
                input_req = RequestData(self.req_reader,
                                        command['id'],
                                        command['name'],
                                        command['bytes'],
                                        command['object'],
                                        password=self.req_password)

                ########
                response_data = self.process_command(input_req)
                #########
                one_item = {
                    "id": input_req.command_id,
                    "line": response_data
                }
                response_json.append(one_item)

                to_return = {
                    "response": response_json
                }
                self.response = to_return
                logging.debug("Response is %s" % json.dumps(response_json))
        except Exception as ex:
            logging.info('Exception in serving response (2), ending thread, cause: %s' % str(ex))

        return

    def process_command(self, input_req):
        """
        Processes command that has been successfully parsed.
        :param input_req:
        :type input_req: RequestData
        :return:
        """
        logging.debug(u"Reader:'{0}',CommandID:'{1}',Command:'{2}'".
                      format(input_req.reader_name, input_req.command_id, input_req.command_name))

        processing_command = input_req.command_name.upper()

        # SEND APDU
        if processing_command == Constant.CMD_APDU:
            token_name = BaseCryptoService.decode_cf_reader(input_req.reader_name)
            response_data = self.signer.apdu(self.upstreamsession, token_name, command=input_req.command_data)
        # get CHAIN
        elif processing_command == Constant.CMD_CHAIN:
            # reader_name = Alias
            response_data = self.signer.chain(input_req.reader_name)
        # ALIAS
        elif processing_command == Constant.CMD_ALIAS:
            aliases = self.signer.aliases()
            response_data = "|".join(aliases)
        # ENUM - get names of all connected tokens
        elif processing_command == Constant.CMD_ENUM:
            readers = self.signer.tokens(input_req.reader_name, input_req.command_data)
            response_data = "|".join(readers)
        # READERS
        elif processing_command == Constant.CMD_LIST:
            readers = self.signer.get_readers(input_req.reader_name, input_req.command_data, input_req.command_object)
            response_data = "|".join(readers)
        # SIGN
        elif processing_command == Constant.CMD_SIGN:
            response_data = self.signer.sign(self.upstreamsession, input_req.reader_name, input_req.command_data,
                                             password=input_req.password)
        # RESET
        elif processing_command == Constant.CMD_RESET:
            token_name = BaseCryptoService.decode_cf_reader(input_req.reader_name)
            response_data = self.signer.reset(self.upstreamsession, token_name)

        elif processing_command == Constant.CMD_CLIENT:
            response_data = 'OK'
        else:  # No valid command found
            response_data = Constant.CMD_RESPONSE_FAIL

        return response_data

    def get_response(self):
        """
        A simple getter for response
        :return:
        """
        return self.response

    def set_lock(self, new_lock):
        """
        Set a lock for the actual card that will be queried
        :param new_lock:
        :type new_lock: Lock
        :return:
        """
        self.lock = new_lock
        pass
