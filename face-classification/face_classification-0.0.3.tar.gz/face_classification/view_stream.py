import socket
import cv2
import pickle
import struct 
from multiprocessing.pool import ThreadPool

pool = ThreadPool(processes=1)
BYTE_SIZE = 4096
MAX_ALLOWED_UNACCEPTANCE = 10

class ViewStream:
    """Uses socket programming to view stream contents from another system
    """

    def __init__(self, PORT):
        """Initializing port parameter
        
        Parameters
        ----------
        PORT : int
            Port address to listen to view stream
        """
        self.first_frame = True
        HOST = ''
        socket_object = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        socket_object.bind((HOST, PORT))
        socket_object.listen(MAX_ALLOWED_UNACCEPTANCE)
        print('Socket now listening')
        self.result = pool.apply_async(self.accept, (socket_object,))
        self.data = b""
        self.payload_size = struct.calcsize(">L")
        print("payload_size: {}".format(self.payload_size))


    def accept(self, socket_object):
        """ Accept socket connection from socket object 
        and return connection object if found

        Parameters
        ----------
        socket_object : Socket Object
            Socket object used to accept connection
        
        Returns
        -------
        Connection object
        """
        return socket_object.accept()


    def get_frame(self):
        """Returns image frame from listening to a port
        
        Returns
        -------
        ndarray
            Image
        """
        
        if self.first_frame == True:    
            self.conn, addr = self.result.get()
            self.first_frame = False

        while len(self.data) < self.payload_size:
            self.data += self.conn.recv(BYTE_SIZE)

        packed_msg_size = self.data[:self.payload_size]
        self.data = self.data[self.payload_size:]
        msg_size = struct.unpack(">L", packed_msg_size)[0]

        while len(self.data) < msg_size:
            self.data += self.conn.recv(BYTE_SIZE)

        frame_data = self.data[:msg_size]
        self.data = self.data[msg_size:]
        frame = pickle.loads(frame_data, fix_imports=True, encoding="bytes")
        frame = cv2.imdecode(frame, cv2.IMREAD_COLOR)

        return frame
