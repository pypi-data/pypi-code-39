import socket
from datetime import datetime
from threading import Thread
from time import sleep
import ssl
from loggingserver import LoggingServer
import urllib.request
import json

class Slave:

    def __init__(self, nickname, password, server_address, server_port):

        self._server_address = server_address
        self._password = password
        self._server_port = server_port
        self._nickname = nickname
        self._logger = LoggingServer.getInstance(nickname)

        self._context = ssl.create_default_context(ssl.Purpose.CLIENT_AUTH)
        self._context.verify_mode = ssl.CERT_REQUIRED
        certurl = "https://raw.githubusercontent.com/vdrhtc/overseer/master/domain.crt"
        self._certfile = urllib.request.urlretrieve(certurl)[0]
        self._context.load_verify_locations(self._certfile)

        self._secure_socket = self._context.wrap_socket(socket.socket())  # instantiate

        self._secure_socket.connect((server_address, server_port))  # connect to the server

        self._stop = False
        self._updater = Thread(target=self._act)
        self._updater.setDaemon(True)

        self._strategies = {"update": self._send_update,
                            "reconnect": self._reconnect,
                            "handshake": self._handshake}
        self._current_strategy = "handshake"

    def launch(self):
        self._stop = False
        self._updater.start()

    def join(self):
        self._updater.join()

    def _act(self):
        while not self._stop:
            try:
                self._strategies[self._current_strategy]()
            except (TimeoutError, ConnectionRefusedError,
                    ConnectionResetError, ConnectionAbortedError,
                    ConnectionError, socket.error) as e:
                self._logger.warn(str(e))
                sleep(15)
                self._current_strategy = "reconnect"
            except Exception as e:
                self._logger.warn(str(e)+" "+str(type(e)))
                print(e)
                break

        self._secure_socket.close()

    def _reconnect(self):
        self._logger.debug("Reconnecting...")

        self._secure_socket.close()
        self._secure_socket = self._context.wrap_socket(socket.socket())
        self._secure_socket.connect((self._server_address, self._server_port))  # connect to the server
        self._current_strategy = "handshake"

    def _handshake(self):
        self._secure_socket.send((self._nickname + "\r\n" + self._password).encode())
        response = self._secure_socket.recv(1024).decode()
        if response == self._nickname:
            self._current_strategy = "update"
            self._logger.debug("Successful handshake!")
        else:
            self._logger.debug(" " + response, end="")
            self._current_strategy = "reconnect"
            sleep(15)

    def _send_update(self):
        self._logger.debug("Sending update, " + str(datetime.now()))
        try:
            data = self.generate_info_message().encode()
        except Exception as e:
            data = str(e).encode()

        self._secure_socket.send(data)
        sleep(15)

    def generate_alert_messages(self):
        return "", "", ""  # "" means no alert, a tuple of strings may be returned though

    def generate_state_message(self):
        return "Example state: I'm OK!"

    def generate_info_message(self):
        s = json.dumps({"sent_at": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                        "state": self.generate_state_message(),
                        "alerts": self.generate_alert_messages()})
        return s
