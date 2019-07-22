import socket
from threading import Thread
from tempfile import mkdtemp
from os import path
from pickle import loads, dumps
from collections import deque


class ChunkWriter(object):
    def __init__(self, file:str, chunk_size:int=1024):
        """
        Initializes the object.
        Opens the target file and prepares properties.
        """
        self.file = open(file, "wb")
        self.running = False
        self.queue = deque()
        self.chunk_size = chunk_size
        self.thread = Thread(target=self._writerThread)
        self.thread.start()
    
    def close(self):
        """
        Wait for the writer thread to finish and close the open file.
        """
        self.running = False
        self.thread.join()
        self.file.close()
    
    def dispatchChunk(self, chunk:tuple):
        """
        Adds chunk to the writer queue.
        Starts the writer thread if it's down.
        """
        self.queue.append(chunk)
    
    def _writerThread(self):
        """
        Runs until a stop is requested and the queue is exhausted.
        """
        self.running = True
        while self.running or len(self.queue):
            if len(self.queue):
                chunk, data = self.queue.popleft()
                self.file.seek(chunk*self.chunk_size)
                self.file.write(data)


class ChunkReceiver(object):
    def __init__(self, writer=ChunkWriter, port=5845, chunksize=1024):
        """
        Initializes the receiver object and socket.
        """
        self.writerConstructor = writer
        self.chunksize = chunksize
        self.packdir = mkdtemp()
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.socket.bind(("", port))
    
    def close(self):
        """
        Close the writer and socket.
        """
        self.writer.close()
        self.socket.close()
    
    def _receiveMeta(self):
        """
        Waits for transfer metadata.
        Confirms receipt and prepares storage.
        """
        data, addr = self.socket.recvfrom(1024)
        self.socket.sendto(b"ACK_META", addr)
        meta = loads(data)
        self.chunks = [False for i in range(meta["length"])]
        self.filename = meta["name"]
        self.master = addr
        self.writer = self.writerConstructor(path.join(
            self.packdir, self.filename
        ))
        self.socket.sendto(b"RDY", addr)
    
    def _receiveData(self):
        """
        Receives the data to write along with the chunk number (because UDP)
        """
        data, _ = self.socket.recvfrom(2048)
        while data != b"EOX":
            capsule = loads(data)
            if not self.chunks[capsule[0]]:
                self.chunks[capsule[0]] = True
                self.writer.dispatchChunk(capsule)
            data, _ = self.socket.recvfrom(2048)
    
    def _checkReceived(self):
        if not all(self.chunks):
            return [i for i, v in enumerate(self.chunks) if not v]
        return False
    
    def _requestMissing(self, missing:list):
        for chunk in missing:
            self.socket.sendto(bytes(str(chunk), "utf-8"), self.master)
    
    def run(self):
        """
        Start receiving a file.
        Blocks until finished.
        """
        self._receiveMeta()
        self._receiveData()
        missed = self._checkReceived()
        while missed:
            self._requestMissing(missed)
            self._receiveData()
            missed = self._checkReceived()
        return path.join(self.packdir, self.filename)


def receive():
    receiver = ChunkReceiver()
    output = receiver.run()
    receiver.close()
    return output
