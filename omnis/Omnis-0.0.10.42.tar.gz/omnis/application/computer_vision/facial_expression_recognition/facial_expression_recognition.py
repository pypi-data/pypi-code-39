from collections import OrderedDict
import json
import os
from math import ceil
import face_recognition
import cv2
import numpy as np
from keras.utils import Sequence
from keras.optimizers import Adam

from .model import regularized_cnn
from ...application import Application
from ....lib.general_lib import get_data_path_type

IMAGE_SHAPE = (48, 48)


class FacialExpressionRecognition(Application):
    def __init__(self, weights_path=None, classes_path=None):
        super().__init__()

        self.model = None
        self.emotions = dict()

        if weights_path is not None and classes_path is not None:
            self.load(weights_path, classes_path)

    def train(self,
              data_path,
              batch_size=1,
              epochs=1,
              verbose=1,
              learning_rate=1e-4):
        train_generator = self.make_train_generator(data_path=data_path,
                                                    batch_size=batch_size)

        steps_per_epoch = len(train_generator)
        self.emotions = train_generator.class_dict
        num_emotions = len(self.emotions)

        if self.model is None:
            self.model = self.create_model(num_emotions)

        self.model.compile(loss='categorical_crossentropy',
                           optimizer=Adam(lr=learning_rate),
                           metrics=['accuracy'])

        self.model.fit_generator(train_generator,
                                 steps_per_epoch=steps_per_epoch,
                                 epochs=epochs,
                                 verbose=verbose)

    def predict(self, data_path):
        data_path_type = get_data_path_type(data_path)
        result_dict = OrderedDict()
        if data_path_type == 'image':
            result_dict[data_path] = self.predict_one_image(data_path)
        elif data_path_type == 'directory':
            images = os.listdir(data_path)
            for image in images:
                image_full_path = os.path.join(data_path, image)
                result_dict[image_full_path] = self.predict_one_image(
                    image_full_path)

        return json.dumps(result_dict, ensure_ascii=False)

    def predict_one_image(self, data_path):
        one_image_dict = OrderedDict()
        image = cv2.imread(data_path, cv2.IMREAD_GRAYSCALE)
        face_locations = face_recognition.face_locations(image)
        for i, face in enumerate(face_locations):
            point_dict = OrderedDict()
            emotion_dict = OrderedDict()
            info_dict = OrderedDict()
            top, right, bottom, left = face
            face_image = image[top: bottom, left: right]
            face_image = face_image.astype('float32')
            face_image /= 255
            face_image = cv2.resize(face_image, (48, 48))
            face_image = np.expand_dims(face_image, axis=-1)
            face_image = np.expand_dims(face_image, axis=0)
            scores = self.model.predict(face_image)
            for j, score in enumerate(scores[0]):
                emotion_dict[self.emotions[j]] = str(score)
            point_dict["top"] = top
            point_dict["right"] = right
            point_dict["bottom"] = bottom
            point_dict["left"] = left

            info_dict["points"] = point_dict
            info_dict["emotions"] = emotion_dict
            one_image_dict[str(i)] = info_dict

        return one_image_dict

    def load(self, weights_path, classes_path):
        emotion_file = open(classes_path, 'r')
        emotions_object = emotion_file.read()
        emotion_file.close()
        emotions = emotions_object.split('\n')

        for i, emotion in enumerate(emotions):
            self.emotions[i] = emotion

        self.model = self.create_model(len(self.emotions))
        self.model.load_weights(weights_path)

    def save(self, weights_path, classes_path):
        self.model.save_weights(weights_path)

        with open(classes_path, 'w') as f:
            for i in range(len(self.emotions)):
                f.write("%s" % self.emotions[i])
                i += 1
                if i != len(self.emotions):
                    f.write("\n")

    def evaluate(self, data_path):
        total_cnt = 0
        correct_cnt = 0
        emotions = os.listdir(data_path)

        for emotion in emotions:
            emotion_path = os.path.join(data_path, emotion)
            images = os.listdir(emotion_path)
            for image in images:
                file_full_path = os.path.join(emotion_path, image)
                img = cv2.imread(file_full_path, cv2.IMREAD_GRAYSCALE)
                face_image = cv2.resize(img, (48, 48))
                face_image = np.expand_dims(face_image, axis=-1)
                face_image = np.expand_dims(face_image, axis=0)
                scores = self.model.predict(face_image)
                highest_score = np.argmax(scores)
                if self.emotions[highest_score] == emotion:
                    correct_cnt += 1
                total_cnt += 1

        print(correct_cnt / total_cnt)

    def create_model(self, num_emotions):
        return regularized_cnn(num_emotions)

    def make_train_generator(self, data_path, batch_size):
        train_datagen = DataGenerator()
        train_generator = \
            train_datagen.flow_from_directory(data_path=data_path,
                                              batch_size=batch_size,
                                              image_shape=IMAGE_SHAPE)
        return train_generator


class DataGenerator(Sequence):
    def __init__(self):
        self.batch_size = 1
        self.image_filenames = []
        self.image_classes = []
        self.class_dict = dict()
        self.image_shape = None
        self.indices = np.arange(len(self.image_filenames))

    def __len__(self):
        return ceil(len(self.image_filenames) / self.batch_size)

    def __getitem__(self, idx):
        indices = self.indices[
            idx * self.batch_size: (idx + 1) * self.batch_size]
        image_names = [self.image_filenames[index] for index in indices]
        image_classes = [self.image_classes[index] for index in indices]

        x = []
        cnt = 0
        for image_name in image_names:
            image = cv2.imread(image_name, cv2.IMREAD_GRAYSCALE)
            image = image.astype('float32')
            image /= 255
            image = cv2.resize(image, self.image_shape)
            image = np.expand_dims(image, axis=-1)
            x.append(image)
            cnt += 1

        y = np.zeros((cnt, len(self.class_dict)), dtype='float')

        i = 0
        for image_class in image_classes:
            y[i, image_class] = 1
            i += 1

        return np.array(x), y

    def on_epoch_end(self):
        np.random.shuffle(self.indices)

    def flow_from_directory(self,
                            data_path,
                            batch_size=1,
                            image_shape=None):
        self.batch_size = batch_size
        self.image_shape = image_shape

        key = 0
        emotions = os.listdir(data_path)
        for emotion in emotions:
            self.class_dict[key] = emotion
            emotion_folder_path = os.path.join(data_path, emotion)
            image_names = os.listdir(emotion_folder_path)
            for image_name in image_names:
                self.image_filenames.append(
                    os.path.join(emotion_folder_path, image_name))

                self.image_classes.append(key)
            key += 1

        self.indices = np.arange(len(self.image_filenames))

        return self
