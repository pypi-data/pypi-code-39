# -*- coding: utf-8 -*-

import os
import cv2
import dlib

from face_recognition import face_locations, face_encodings
from face_recognition.face_recognition_cli import image_files_in_folder

def _create_dir_if_not_exists(folder_name):
        """ Checks if a folder exists and creates if not.
        
        Parameters
        ----------
        folder_name : str
            Path to folder.
        """
        if not (os.path.isdir(folder_name)):
                os.mkdir(folder_name)


def _extract_encodings(input_folder):
        """ Extract encodings from each face in a given image and returns the encoding corresponding to given images.
        
        Parameters
        ----------
        input_folder : str
            Path to input folder directory.
        
        Returns
        -------
        list, list
            List of images and corresponding encodings.
        """
        encodings = []
        images = []

        # Load the images from input folder
        for file_name in image_files_in_folder(input_folder):
                print("Processing file: {}".format(file_name))
                image = cv2.imread(file_name)
                bounding_boxes = face_locations(image)

                # Only clustering images with single face 
                if len(bounding_boxes) != 1:
                        print("Multiple or zero faces detected in this file: {}. Skipping this one.".format(file_name))
                        continue
                
                # Converting the python-instance encoding to dlib.vector for further classification using dlib
                encoding = dlib.vector(face_encodings(image, bounding_boxes)[0])
                encodings.append(encoding)
                images.append(image)
        
        return encodings, images


def _save_images(images, labels, output_folder):
        """ Saves images in its own cluster folder.
        
        Parameters
        ----------
        images : list
            List of RGB images.
        labels : list
            Cluster label for each image.
        output_folder : str
            Path to output directory.
        """
        for i, (image, label) in enumerate(zip(images, labels)):
                output_path = os.path.join(output_folder, 'output' + str(label))
                _create_dir_if_not_exists(output_path)
                cv2.imwrite(os.path.join(output_path, str(i) + '.jpg'), image)

        
def cluster_faces(input_folder, output_folder='output_clusters', threshold_distance=0.4):
        """ Clusters unknown faces in a given folder, using chinese whispers algorithm and 
             keeps each cluster of faces in a separate folder.
        
        Parameters
        ----------
        input_folder : str
            Path to input directory.
        output_folder : str
            Path to output directory.
        """

        _create_dir_if_not_exists(output_folder)

        # Extract embeddings of each face
        encodings, images = _extract_encodings(input_folder)

        # Cluster the faces using chinese wishpers algorithm(outputs each image cluster-label)
        # The model was trained using 0.6 distance threshold, keeping it at 0.4 for maximum precision.
        labels = dlib.chinese_whispers_clustering(encodings, threshold_distance)       

        # Converting labels into set (list to set) to acquire the total number of classes/clusters
        total_clusters = len(set(labels))
        print("Number of clusters: {}".format(total_clusters))
        _save_images(images, labels, output_folder)
