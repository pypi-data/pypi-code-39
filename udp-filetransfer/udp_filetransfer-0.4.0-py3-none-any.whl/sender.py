import socket
from threading import Thread
from pickle import loads, dumps
from os import path
from math import ceil

def opportunistic_wrapper(i):
    try:
        from tqdm import tqdm
        return tqdm(i)
    except ImportError:
        return i

class ChunkSender(object):
    def __init__(
        self,
        filename:str,
        port=5845,
        chunksize=1024,
        timeout=2,
        iterable_wrapper=opportunistic_wrapper
        ):
        """
        Initializes the object.
        Opens the file.
        Prepares the socket.
        """
        self.port = port
        self.chunksize = chunksize
        self.timeout = 2
        self.file = open(filename, "rb")
        self.iterable_wrapper = iterable_wrapper
        sck = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sck.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)
        sck.bind(("0.0.0.0", 5846))
        self.socket = sck
    
    def close(self):
        self.socket.close()
        self.file.close()

    def _sendMeta(self):
        size = self.file.seek(0, 2)
        self.file.seek(0)
        _, filename = path.split(self.file.name)
        meta = {
            "length": ceil(size / self.chunksize),
            "name": filename
        } 
        self.chunks = meta["length"]
        self.socket.sendto(dumps(meta), ("255.255.255.255", self.port))
    
    def _receiveAcknowledge(self):
        receiverCount = 0
        readyCount = 0
        self.socket.settimeout(self.timeout)
        try:
            while True:
                data, _ = self.socket.recvfrom(1024)
                if data == b"ACK_META":
                    receiverCount = receiverCount + 1
                if data == b"RDY":
                    readyCount = readyCount + 1
        except socket.timeout:
            pass
        self.socket.settimeout(None)
        if receiverCount > readyCount:
            for _ in self.iterable_wrapper(
                range(receiverCount - readyCount)
            ):
                data, _ = self.socket.recvfrom()
        return bool(receiverCount)
    
    def _sendAll(self):
        for chunk in range(self.chunks):
            data = self.file.read(self.chunksize)
            self.socket.sendto(
                dumps((chunk, data)),
                ("255.255.255.255", self.port)
            )
    
    def _receiveMissed(self):
        self.socket.settimeout(self.timeout)
        self.socket.sendto(b"EOX", ("255.255.255.255", self.port))
        missed = set()
        try:
            while True:
                data, _ = self.socket.recvfrom(1024)
                missed.add(int(data))
        except socket.timeout:
            pass
        self.socket.settimeout(None)
        return missed
    
    def _sendChunks(self, chunks):
        for chunk in self.iterable_wrapper(chunks):
            self.file.seek(chunk*self.chunksize)
            self.socket.sendto(
                dumps((chunk, self.file.read(self.chunksize))),
                ("255.255.255.255", self.port)
            )
    
    def send(self):
        """
        Send the file to anyone who's receiving.

        Throws a TimeoutError if no one is listening.
        """
        self._sendMeta()
        if self._receiveAcknowledge():
            self._sendAll()
            missed = self._receiveMissed()
            while len(missed):
                self._sendChunks(missed)
                missed = self._receiveMissed()
            return
        raise TimeoutError("Timed out while waiting for ACK from receivers. \
            No receivers found.")


def send(filename:str):
    """
    Arranges for initialization of the ChunkSender object,
    the file's transfer, and the object's proper closure.
    """
    sender = ChunkSender(filename)
    sender.send()
    sender.close()
