import cv2
import socket
import struct
import pickle

class StreamFrame:
    """ Uses socket programming to stream frames over another computer
    """
    def __init__(self, ip, PORT):
        """Initialize parameters for sending frame stream
        
        Parameters
        ----------
        ip : str
            IP address of the where frames are sent
        PORT : int
            Port address to use to send frames
        """

        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.client_socket.connect((ip, PORT))
        self.encode_param = [int(cv2.IMWRITE_JPEG_QUALITY), 90]
   

    def stream_frame(self, frame):
        """ Takes a frame and sends it into given ip address on the specified port using sockets
        
        Parameters
        ----------
        frame : ndarray
            Image or a picture to be sent off
        """
        _, frame = cv2.imencode('.jpg', frame, self.encode_param)
        data = pickle.dumps(frame, 0)
        size = len(data)
        self.client_socket.sendall(struct.pack(">L", size) + data)


    def receive(self):
        """ Returns  a string received from the connection 
        
        Returns
        -------
        str
            String containing the prediction from server
        """
        result_bytes = self.client_socket.recv(4096)  
        receive_list = pickle.loads(result_bytes)

        return receive_list
