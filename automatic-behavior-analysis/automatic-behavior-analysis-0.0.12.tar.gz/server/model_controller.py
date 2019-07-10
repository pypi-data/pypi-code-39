#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Copyright (c) Wed Oct 24 18:58:55 2018 Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>

Created on Wed Oct 24 18:58:55 2018
@author: Sinitca Alekandr <amsinitca@etu.ru, siniza.s.94@gmail.com>
"""

__author__ = 'Sinitca Alekandr'
__contact__ = 'amsinitca@etu.ru, siniza.s.94@gmail.com'
__copyright__ = 'Sinitca Alekandr'
__license__ = 'Proprietary'
__date__ = 'Wed Oct 24 18:58:55 2018'
__version__ = '0.1'

import sys
import os
import numpy as np
import cv2
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '1'
import tensorflow as tf
from PIL import Image
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util
from object_detection.utils import visualization_utils as vis_util
from datetime import datetime
import json

from keras.models import model_from_json
from util.geom_tools import rect_overlap, rect_area

def find_model_root(current_dir, module_dir):
    def paths():
        yield os.path.join(current_dir, module_dir)
        yield os.path.join(current_dir, '..', module_dir)

    for path in paths():
        if os.path.isdir(path):
            return os.path.abspath(path)

    raise RuntimeError("Unable to find model directory")

class ModelController():
    def __init__(self, config, noisy=False):
        model_root = config.model_root or find_model_root(os.getcwd(), 'AI_module')
        sub = lambda key: config[key].replace('{model_root}', model_root)

        self._noisy = noisy

        model_version = config.get('model_version')

        if model_version is None:
            self._use_classifier = config.get('use_classifier', False)
            self._use_eye_detector = config.get('use_eye_detector', False)
        elif model_version == 1:
            self._use_classifier = False
            self._use_eye_detector = False
        elif model_version == 2:
            self._use_classifier = True
            self._use_eye_detector = False
        else:
            raise RuntimeError("Invalid model version: {}".format(model_version))

        self._model_path_detector_graph = sub('model_path_detector_graph')
        self._model_path_detector_label_map = sub('model_path_detector_label_map')
        self._target_classes = config.target_classes
        self._eye_target_classes = config.eye_target_classes
        self._box_overlap_threshold = config.get('box_overlap_threshold', 0.9)
        self._convert_to_grayscale = config.get('convert_to_grayscale', False)
        print("Using classifier: {}, using eye detector: {}".format(self._use_classifier, self._use_eye_detector))
        print("Current directory:", os.getcwd())

        # Testing
        # self._model_path_detector_graph = "ssd_resnet50.pb"
        # self._model_path_detector_label_map = "mscoco_label_map.pbtxt"
        # self._target_classes =  (17, 18)

        self._label_map = label_map_util.load_labelmap(self._model_path_detector_label_map)
        self._categories = label_map_util.convert_label_map_to_categories(self._label_map, max_num_classes=1, use_display_name=True)
        self._category_index = label_map_util.create_category_index(self._categories)

        if self._use_classifier: # the classifier is in a separate model
            self._model_path_classifier_weights = sub('model_path_classifier_weights')
            self._model_path_classifier_scheme = sub('model_path_classifier_scheme')
            self._img_width, self._img_height = 300, 300
            self._classifier = self.get_keras_model_from_file(self._model_path_classifier_scheme, self._model_path_classifier_weights)

        if self._use_eye_detector:
            self._model_path_eye_detector_graph = sub('model_path_eye_detector_graph')
            self._model_path_eye_detector_label_map = sub('model_path_eye_detector_label_map')
            self._eye_detection_graph = self.load_detector(self._model_path_eye_detector_graph, "eye")
            self._eye_detection_sess = tf.Session(graph=self._eye_detection_graph)

        # self._detection_graph = tf.Graph()

        # with self._detection_graph.as_default():
        #     od_graph_def = tf.GraphDef()
        #     print("Loading object detection graph from " + self._model_path_detector_graph)
        #     with tf.gfile.GFile(self._model_path_detector_graph, 'rb') as fid:
        #         serialized_graph = fid.read()
        #         od_graph_def.ParseFromString(serialized_graph)
        #         tf.import_graph_def(od_graph_def, name='')
        #     self._sess = tf.Session()
        self._detection_graph = self.load_detector(self._model_path_detector_graph, "object")
        with self._detection_graph.as_default():
            self._sess = tf.Session()

    def log(self, *args):
        if self._noisy:
            print(*args)

    def load_detector(self, graph_path, tag):
        graph = tf.Graph()

        with graph.as_default():
            od_graph_def = tf.GraphDef()
            print("Loading {} detection graph from {}".format(tag, graph_path))
            with tf.gfile.GFile(graph_path, 'rb') as fid:
                serialized_graph = fid.read()
                od_graph_def.ParseFromString(serialized_graph)
                tf.import_graph_def(od_graph_def, name='')

        return graph

    def get_keras_model_from_file(self, model_file_name, weight_file_name):
        print("Loading state classifier model from " + model_file_name)
        json_model_file = open(model_file_name, "r")
        loaded_model_json = json_model_file.read()
        json_model_file.close()
        new_model = model_from_json(loaded_model_json)
        self.log("Loading state classifier weights from " + weight_file_name)
        new_model.load_weights(weight_file_name)
        return new_model

    def crop_image_process(self, image):
        x = cv2.resize(image, (self._img_width, self._img_height))
        x = cv2.cvtColor(x, cv2.COLOR_BGR2GRAY)
        if self._convert_to_grayscale:
            x = x.reshape((self._img_width, self._img_height, 1))
        else:
            x = cv2.cvtColor(x, cv2.COLOR_GRAY2BGR)
        x = x * 1. / 255
        x = x.reshape((1,) + x.shape)  # this is a Numpy array with shape (1, x, y, z)
        pr = self._classifier.predict(x)
        # self.log("- classifier output: {}".format(pr))
        return pr[0][0] > 0.5

    # def run_detector(self, graph, pred, callback):
    def run_detector(self, graph, sess, image_np):
        ops = graph.get_operations()
        all_tensor_names = {output.name for op in ops for output in op.outputs}
        tensor_dict = {}
        for key in ['num_detections', 'detection_boxes', 'detection_scores', 'detection_classes', 'detection_masks']:
            tensor_name = key + ':0'
            if tensor_name in all_tensor_names:
                tensor_dict[key] = graph.get_tensor_by_name(tensor_name)
        if 'detection_masks' in tensor_dict:
            detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
            detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
            real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
            detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
            detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
            detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(detection_masks, detection_boxes, image_np.shape[0], image_np.shape[1])
            detection_masks_reframed = tf.cast(tf.greater(detection_masks_reframed, 0.5), tf.uint8)
            tensor_dict['detection_masks'] = tf.expand_dims(detection_masks_reframed, 0)

        image_tensor = graph.get_tensor_by_name('image_tensor:0')
        # Запуск поиска объектов на изображении
        output_dict = sess.run(tensor_dict, feed_dict={image_tensor: np.expand_dims(image_np, 0)})

        # Преобразуем выходные тензоры типа float32 в нужный формат
        output_dict['num_detections'] = int(output_dict['num_detections'][0])
        output_dict['detection_classes'] = output_dict['detection_classes'][0].astype(np.uint8)
        output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
        output_dict['detection_scores'] = output_dict['detection_scores'][0]
        if 'detection_masks' in output_dict:
            output_dict['detection_masks'] = output_dict['detection_masks'][0]

        # return [callback(output_dict, i) for i in range(output_dict['num_detections']) if pred(output_dict, i)]
        return output_dict

    def full_image_process(self, image_np, detect_inner_objects=False):
        # Используем модель (граф TensorFlow), которую ранее загрузили в память
        # with self._detection_graph.as_default():
        # Все операции в TensorFlow выполняются в сессии
        # Готовим операции и входные данные
        # print("image shape:", image_np.shape)
        # if self._convert_to_grayscale and image_np.shape[2] > 1:
        #     image_np = cv2.cvtColor(image_np, cv2.COLOR_BGR2GRAY)
        #     print("image shape after conversion:", image_np.shape)
        #     image_np = image_np.reshape(image_np.shape[0], image_np.shape[1], 1)
        #     print("image shape after second conversion:", image_np.shape)
        #     # image_np = cv2.cvtColor(image_np, cv2.COLOR_GRAY2BGR)
        #     # print("image shape after third conversion:", image_np.shape)

        output_dict = self.run_detector(self._detection_graph, self._sess, image_np)

        result = []
        for i in range(output_dict['num_detections']):
            if output_dict['detection_classes'][i] in self._target_classes and output_dict['detection_scores'][i] > 0.5:
                self.log("- detection box {}: {}".format(i, output_dict['detection_boxes'][:][i]))

                if self._use_classifier or self._use_eye_detector:
                    cropped_img = self._crop_image(image_np, output_dict['detection_boxes'][:][i])

                verd = self.crop_image_process(cropped_img) if self._use_classifier else output_dict['detection_classes'][i] == 2
                children = self.run_eye_detector(cropped_img) if self._use_eye_detector and detect_inner_objects else None

                self.log("- asleep: {}".format(verd))
                result.append((output_dict['detection_boxes'][:][i], output_dict['detection_scores'][i], verd, children))

        return result

    def run_eye_detector(self, image_np):
        print("Running eye detection")
        output_dict = self.run_detector(self._eye_detection_graph, self._eye_detection_sess, image_np)

        result = []
        for i in range(output_dict['num_detections']):
            if output_dict['detection_classes'][i] in self._eye_target_classes and output_dict['detection_scores'][i] > 0.5:
                self.log("- eye detection box {}: {}".format(i, output_dict['detection_boxes'][:][i]))

                # if self._use_eye_classifier:
                #     cropped_img = self._crop_image(image_np, output_dict['detection_boxes'][:][i])

                verd = output_dict['detection_classes'][i] == 2

                # self.log("- eye open: {}".format(verd))
                result.append((output_dict['detection_boxes'][:][i], output_dict['detection_scores'][i], verd))
                print("Eye detection result:", result[-1])

        return result

    def _crop_image(self, image_np, bourder):
        y1 = int(image_np.shape[0] * bourder[0])
        x1 = int(image_np.shape[1] * bourder[1])
        y2 = int(image_np.shape[0] * bourder[2])
        x2 = int(image_np.shape[1] * bourder[3])
        return np.copy(image_np[y1:y2, x1:x2])

    def _remove_overlapping_boxes(self, report):
        remove = set()
        for i in range(len(report)):
            for j in range(i + 1, len(report)):
                box_i = report[i][0]
                box_j = report[j][0]
                area_i = rect_area(box_i)
                area_j = rect_area(box_j)
                common_area = rect_overlap(box_i, box_j)
                if report[i][2] != report[j][2] and (common_area / area_i > self._box_overlap_threshold or common_area / area_j > self._box_overlap_threshold):
                    # Too much overlap between boxes
                    # Remove the box with the smaller detection rate
                    # If detection rates identical, remove the smaller box
                    # If the area is also identical, we leave both boxes
                    if report[i][1] < report[j][1]:
                        remove.add(i)
                    elif report[j][1] < report[i][1]:
                        remove.add(j)
                    elif area_i < area_j:
                        remove.add(i)
                    elif area_j < area_i:
                        remove.add(j)

        return [r for i, r in enumerate(report) if i not in remove]

    def _transform_eye_report(self, report):
        result = []

        for ind, r in enumerate(report):
            item = {}
            item['id'] = ind
            self.log('- eye detection result {}: {}'.format(ind, r))
            item['y1'] = float(r[0][0])
            item['x1'] = float(r[0][1])
            item['y2'] = float(r[0][2])
            item['x2'] = float(r[0][3])
            item['rate'] = float(r[1])
            item['state'] = 'open' if r[2] else 'closed'
            item['category'] = 'eye'
            result.append(item)

        return result

    def _prepare_report_to_client(self, report):
        '''
        JSON_EXAMPLE
        {"dogs":
            [
                {
                    "id": 1,
                    "rate":0.6,
                    "x1": 0.5,
                    "y1": 0.5,
                    "x2": 0.6,
                    "y2": 0.6,
                    "state": "sleep"
                },
                {
                    "id": 2,
                    "rate":0.8,
                    "x1": 0.2,
                    "y1": 0.2,
                    "x2": 0.3,
                    "y2": 0.3,
                    "state": "awake"
                }
            ]
        }
        '''
        result = []
        report = self._remove_overlapping_boxes(report)

        for ind, r in enumerate(report):
            item = {}
            item['id'] = ind
            self.log('- detection result {}: {}'.format(ind, r))
            item['y1'] = float(r[0][0])
            item['x1'] = float(r[0][1])
            item['y2'] = float(r[0][2])
            item['x2'] = float(r[0][3])
            item['rate'] = float(r[1])
            item['state'] = 'sleep' if r[2] else 'awake'
            item['category'] = 'dog'
            item['children'] = self._transform_eye_report(r[3]) if r[3] else None
            result.append(item)

        return { 'dogs': result } # TOOD: replace 'dogs' with 'objects'

    def _decode_image(self, raw_img):
        nparr = np.frombuffer(raw_img, np.uint8)
        img_np = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
        return img_np

    def _get_np_image(self, np_image):
        success, encoded_image = cv2.imencode('.jpg', np_image)
        return encoded_image.tobytes()

    def process_image(self, payload, header=None):
        image = self._decode_image(payload)
        detect_inner_objects = header and header.get('detect_inner_objects')
        report = self.full_image_process(image, detect_inner_objects)
        return self._prepare_report_to_client(report)

    def process_decoded_image(self, image):
        report = self.full_image_process(image)
        return self._prepare_report_to_client(report)
