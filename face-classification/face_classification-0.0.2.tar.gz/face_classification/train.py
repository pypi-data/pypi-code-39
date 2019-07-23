import os
import pickle

import face_recognition
from sklearn import neighbors
from face_recognition.face_recognition_cli import image_files_in_folder

def train(train_dir, model_file_name='./model.clf', n_neighbors=2):
    """
    Train a k-nearest neighbors classifier for face recognition and save the model as a pickle file in model_file_name.

    Paramters
    ---------
    train_dir : string
        Directory that contains sub-directories for each person's single image with the folder name as the person's name or identifier name.
    
    model_file_name : string
        The location to save the model.
    
    n_neighbors : int, optional
        The number of neighbors to be used in knn algorithm.
    """

    X = []
    y = []
    
    # Loop through each person in the training set
    for class_dir in os.listdir(train_dir):
        if not os.path.isdir(os.path.join(train_dir, class_dir)):
            continue

        # Loop through each training image for the current person
        for img_path in image_files_in_folder(os.path.join(train_dir, class_dir)):
            image = face_recognition.load_image_file(img_path)
            bounding_boxes = face_recognition.face_locations(image)

            if len(bounding_boxes) == 1:
                # Add face encoding for current image to the training set
                encodings = face_recognition.face_encodings(image, known_face_locations=bounding_boxes)
                X.append(encodings[0])
                y.append(class_dir)

    # Create and train the KNN classifier
    knn_clf = neighbors.KNeighborsClassifier(n_neighbors=n_neighbors, algorithm='ball_tree', weights='distance')
    knn_clf.fit(X, y)

    # Save the trained KNN classifier
    with open(model_file_name, 'wb') as f:
        pickle.dump(knn_clf, f)
