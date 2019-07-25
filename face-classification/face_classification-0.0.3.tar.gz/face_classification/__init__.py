"""
    Face Classification module for Python
    ==================================
    face_classification is a Python module integrating classical face detection
    and classification algorithms using tightly-knit package like dlib,
    openCV and face_recognition. It aims to provide simple and efficient solutions 
    to face classification problems that are accessible to everybody and reusable in 
    various contexts.
"""

from face_classification.train import train
from face_classification.classifier import FaceClassifier, get_face_boundings, get_face_embeddings, load_image_file
from face_classification.face_clustering import cluster_faces
from face_classification.stream import StreamFrame
from face_classification.view_stream import ViewStream
from face_classification.recognition_server import RecognitionServer
