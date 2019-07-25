import pickle

from face_recognition import face_locations, face_encodings, load_image_file


def get_face_boundings(img):
    """ 
    Returns the face boundings from image.

    Parameters
    ----------

    img : float array of image of 3 channel
        The image should be in RGB format 

    Returns
    -------

    face_boundings : list
        A list of dictionaries with face bounding boxes.
    """
    face_boundings = face_locations(img)
    cordinates = ('y1', 'x2', 'y2', 'x1')
    face_bounding_dicts = [dict(zip(boundings, cordinates)) for boundings in face_boundings]

    return face_bounding_dicts


def get_face_embeddings(img, bounding_boxes):
    """ 
    Returns the encoding from the image and face location.

    Parameters
    ----------

    img : float array of image of 3 channel
        The image should be in RGB format and the pixels value between 0 and 1.
    
    bounding_boxes : array of size [n, 4] where n is the number of faces
        Location of the faces returned from the get_face_boudings function.

    Returns
    -------

    embeddings : array of formatter python size [n, 128] where n is the number of faces
        The face embeddings from cropped faces ina image.
    """
    embeddings = face_encodings(img, known_face_locations=bounding_boxes)

    return embeddings


class FaceClassifier:
    """
    Face recognition model to predict the faces in the images passed to it and return the predicted faces' location,
    the face embedding and the predicted class.
    """
    
    def __init__(self, model_path=None, threshold_value=0.4):
        """
        Initialising parameters to the class.

        Parameters
        -----------

        model_path : string
            The location of the trained model's pickle file.
            Training can be done from train_model module of this package which requires location to store the pickle file.

        threshold_value : float, optional
            Show prediction only if the distance between the nearest point to the predicted embedding of image is less than the threshold_value.
            0.4 is default as it works well in most of the cases and is better for precision.
        """        
        if model_path is not None:
            with open(model_path, 'rb') as f:
                self.model = pickle.load(f)
        self.threshold_value = threshold_value


    def classify_face(self, embeddings):
        """ 
        Classify face from face embedding.

        Parameters
        ----------

        embeddings : array of size [n, 128] where n is the number of faces

        Returns
        -------

        predictions : array
            The prediction of the faces.     
        """
        closest_distances = self.model.kneighbors(embeddings, n_neighbors=1)
        matches = [closest_distances[0][i][0] <= self.threshold_value for i in range(len(embeddings))]
        predictions = [pred if rec else 'unknown' for pred, rec in zip(self.model.predict(embeddings), matches)]

        return predictions


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
        predictions : dict
            The prediction zipped with bounding boxes is returned.
        """
        boundings = face_locations(img)
    
        predictions = []     
        if len(boundings) > 0:            
            embeddings = face_encodings(img, known_face_locations=boundings)
            predictions = self.classify_face(embeddings)
                
        return dict(zip(predictions, boundings))
