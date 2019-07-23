# __all__ = ["AuspexInstrumentHub"]

# import zmq
# import random
# import socket
# import time

# from . import client_classes, server_classes

# def lookup_instr(address, server=False):
#     classes = server_classes if server else client_classes
#     available_addresses = [e['address'] for e in available_instruments_local]
#     inst = [inst for inst in available_instruments_local if inst['address'] == address]
#     if len(inst) == 0:
#         return None
#     inst = inst[0]
#     instr_class = [v for k,v in classes.items() if inst['model'] in k][0]
#     return instr_class

# def get_servers_instruments(address):
#     context = zmq.Context()
#     socket = context.socket(zmq.REQ)
#     socket.connect(f"tcp://{address}:7777")
#     token = f"{random.getrandbits(64):016x}"
#     socket.send_pyobj({'msg_type': "server_control", 'cmd_name': "list_instruments_local", 'token': token})
#     message = socket.recv_pyobj()
#     if message['token'] != token:
#         raise Exception("Received wrong token in reply!")
#     if not message['success']:
#         raise Exception("Command Failed")
#     return message['return_value']

# def find_remote_instruments(address=None, broadcast='255.255.255.255', port=7777):
#     local_addrs = socket.gethostbyname_ex(socket.gethostname())[-1]
#     if address is None:
#         for addr in local_addrs:
#             if not addr.startswith('127'):
#                 address = addr
#     # Create UDP socket
#     handle = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)
#     # Ask operating system to let us do broadcasts from socket
#     handle.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
#     handle.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
#     # Register poller
#     poller = zmq.Poller()
#     poller.register(handle, zmq.POLLIN)

#     ping_at = time.time()
#     servers = []

#     handle.sendto('!'.encode(), 0, (broadcast, port))
#     while time.time() - ping_at < 1.0:
#         try:
#             events = dict(poller.poll(1000))
#         except KeyboardInterrupt:
#             print("interrupted")
#             break
#         if handle.fileno() in events:
#             buf, addrinfo = handle.recvfrom(8192)
#             servers.append(addrinfo[0])

#     instruments = {}
#     for server in servers:
#         server_instrs = get_servers_instruments(server)
#         for i in server_instrs:
#             i['server'] = server
#         instruments[server] = server_instrs

#     return servers, instruments

# class AuspexInstrumentHub():
#     def __init__(self):
#         self.find_instruments()
    
#     def find_instruments(self):
#         self.servers, self.instruments = find_remote_instruments()

#     # def connect():
#     #     # Should find servers and choose the "best" one
#     #     pass
   
#     # def connect_to(self, address, port=7777):
#     #     self.context = zmq.Context()
#     #     self.socket = self.context.socket(zmq.REQ)
#     #     self.socket.connect(f"tcp://{address}:{port}")

#     # def get_instruments(self, with_remote=True):
#     #     if with_remote:
#     #         return self.send({'msg_type': "server_control", 'cmd_name': "list_instruments"})
#     #     else:
#     #         return self.send({'msg_type': "server_control", 'cmd_name': "list_instruments_local"})
#     # def 

#     def update_instruments(self):
#         for server in self.servers:
#             context = zmq.Context()
#             socket = context.socket(zmq.REQ)
#             socket.connect(f"tcp://{server}:{7777}")
#             token = f"{random.getrandbits(64):016x}"
#             msg = {'msg_type': "server_control",
#                    'cmd_name': "update_instruments",
#                    'token': token}
#             socket.send_pyobj(msg)
#             rep = socket.recv_pyobj()
#             if rep['token'] != token:
#                 raise Exception("Received wrong token in reply!")
#             if not rep['success']:
#                 raise Exception("Command Failed")

    # def send(self, msg):
    #     msg['token'] = f"{random.getrandbits(64):016x}"
    #     self._snd(msg)
    #     return self._rcv(msg['token'])
   
    # def _snd(self, msg):
    #     self.socket.send_pyobj(msg)

    # def _rcv(self, token):
    #     # print("Manager rcv")
    #     message = self.socket.recv_pyobj()
    #     # print("message", message)
    #     if message['token'] != token:
    #         raise Exception("Received wrong token in reply!")
    #     if not message['success']:
    #         raise Exception("Command Failed")
    #     return message['return_value']