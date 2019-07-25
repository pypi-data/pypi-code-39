import cv2
import struct
import pickle

from face_classification.classifier import FaceClassifier, get_face_boundings, get_face_embeddings
from face_classification.view_stream import ViewStream

class RecognitionServer(FaceClassifier, ViewStream):

    def __init__(self, model_path, PORT):
        FaceClassifier.__init__(self, model_path)
        ViewStream.__init__(self, PORT)


    def predict(self, img):
        """
        Returns the predicted classes of the faces in the image passed to it.
        
        Parameters
        ----------
        
        img : float array of image of 3 channel
            The image should be in RGB format and the pixels value between 0 and 1.
        ----------

        Returns
        -------

        boundings : array of shape [n, 4] where n is the number of faces in the image
            The face boundings is returned in (y1, x2, y2, x1)
        
        names : array
            The prediction of the faces. 
        """
        boundings = get_face_boundings(img)

        names = []     
        if len(boundings) > 0:            
            embeddings = get_face_embeddings(img, boundings)
            names = FaceClassifier.classify_face(self, embeddings)
                
        return names, boundings


    def get_frame(self, BYTE_SIZE=4096):
        """ Returns image frame from listening to a port
        
        Parameters
        ----------
        BYTE_SIZE : int, optional
            Size of bytes to receive at a time, by default 4096
        
        Returns
        -------
        ndarray
            Image

        conn
            Socket connection object
        """
        
        if self.first_frame:    
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

        return frame, self.conn


    def detect(self):
        """ Receives the incoming picture frame and sends the detected face bounding boxes through socket
        """
        frame, conn = self.get_frame()
        boundings = get_face_boundings(frame)
        boundings_bytes = pickle.dumps(boundings)
        conn.sendall(boundings_bytes)


    def recognize(self):
        """ Receives the incoming picture frame and sends the detected people names through socket
        """
        frame, conn = self.get_frame()
        names = self.predict(frame)
        names_bytes = pickle.dumps(names)
        conn.sendall(names_bytes)
