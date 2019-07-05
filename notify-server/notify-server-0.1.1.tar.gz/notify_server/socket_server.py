import json
import socket
from threading import Thread

from notify_cli.binary_protocol import BinaryProtocol
from notify_server.events import EventSystem


class SocketServer:
    def __init__(self, host: str, port: int, event_system: EventSystem):
        self.server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.server.bind((host, port))
        self.server.listen()
        self.event_system = event_system

    def start(self):
        Thread(target=self._run, daemon=True).start()

    def _run(self):
        while True:
            client_sock, address = self.server.accept()
            Thread(
                target=self._handle_client,
                args=(client_sock,),
                daemon=True
            ).start()

    def stop(self):
        self.server.close()

    def _handle_client(self, client_socket):
        client = BinaryProtocol(client_socket)
        callbacks = {}
        try:
            while True:
                msg = client.receive()
                try:
                    json_data = json.loads(msg)
                    msg_type = json_data['type']
                    if msg_type == 'subscribe':
                        def callback(event, c=client):
                            c.send(json.dumps(event))

                        event = json_data['event']
                        self.event_system.subscribe(event, callback)
                        callbacks[event] = callback
                    elif msg_type == 'unsubscribe':
                        event = json_data['event']
                        if event in callbacks:
                            self.event_system.unsubscribe(event, callbacks[event])
                            del callbacks[event]
                    elif msg_type == 'event':
                        self.event_system.send(json_data['event'], json_data['data'])

                except (ValueError, KeyError):
                    continue

        except ConnectionAbortedError:
            return
        finally:
            for event, callback in callbacks.items():
                self.event_system.unsubscribe(event, callback)
