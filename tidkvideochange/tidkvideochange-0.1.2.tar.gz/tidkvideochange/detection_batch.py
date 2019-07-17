import time

try:
    import importlib.resources as pkg_resources
except ImportError:
    # Try backported to PY<37 `importlib_resources`.
    import importlib_resources as pkg_resources

import numpy as np
import tensorflow as tf
from PIL import Image

from . import weights

# Path to frozen detection graph. This is the model retrained on text data
#PATH_TO_CKPT = './weights/frozen_inference_graph.pb'
with pkg_resources.path(weights, "frozen_inference_graph.pb") as path:
    PATH_TO_CKPT = str(path.resolve())

DEFAULT_SCORE_THRESHOLD=0.4

def timefunc(f):
    def f_timer(*args, **kwargs):
        start = time.time()
        result = f(*args, **kwargs)
        end = time.time()
        print(f.__name__, 'took', end - start, 'time')
        return result
    return f_timer

detection_graph = None
od_graph_def = None
serialized_graph = None

def prepare_model():
  # Load a (frozen) Tensorflow model into memory.
  global detection_graph
  global od_graph_def
  global serialized_graph
  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_CKPT, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')
      

def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def decode_box_coordinates(image, file_boxes):
    width, height = image.size
    new_boxes = []
    for box in file_boxes:
        #print("box" + str(box))
        ymin = box[0] * height
        xmin = box[1] * width
        ymax = box[2] * height
        xmax = box[3] * width
        new_boxes.append((xmin,ymin,xmax,ymax))
    return new_boxes

@timefunc
def detect(image_paths, score_threshold = DEFAULT_SCORE_THRESHOLD):
    with detection_graph.as_default():
        with tf.Session(graph=detection_graph) as sess:
            
            # Definite input and output Tensors for detection_graph
            image_tensor = detection_graph.get_tensor_by_name('image_tensor:0')
            detection_boxes = detection_graph.get_tensor_by_name('detection_boxes:0')
            detection_scores = detection_graph.get_tensor_by_name('detection_scores:0')
            detection_classes = detection_graph.get_tensor_by_name('detection_classes:0')
            num_detections = detection_graph.get_tensor_by_name('num_detections:0')

            image_np_expanded = None
            for path in image_paths:
              image = Image.open(path)
              image_np = load_image_into_numpy_array(image)
              if image_np_expanded is not None:
                image_np_expanded = np.concatenate([image_np_expanded, np.expand_dims(image_np, axis=0)], axis=0)
              else:
                image_np_expanded = np.expand_dims(image_np, axis=0)
            #image = Image.open(image_path)
            #image_np = load_image_into_numpy_array(image)
            # Expand dimensions since the model expects images to have shape: [1, None, None, 3]
            #image_np_expanded = np.expand_dims(image_np, axis=0)
            # Actual detection.
            (file_boxes, file_scores, file_classes, file_num) = sess.run(
              [detection_boxes, detection_scores, detection_classes, num_detections],
              feed_dict={image_tensor: image_np_expanded})
            #return boxes, scores, classes, num
            #print(file_scores)
            #print(file_boxes)
            

            #top_box_indices = file_scores[:,0] > score_threshold
            top_box_indices = file_scores > score_threshold
            #top_box_indices = np.concatenate([np.resize(top_box_indices, (image_np_expanded.shape[0], 1)),np.zeros((image_np_expanded.shape[0], 99), dtype=bool)], axis=1)
            #top_box_indices = np.array([[True] + 99*[False], [True] + 99*[False], [True] + 99*[False], [True] + 99*[False]])
            #print(top_box_indices)

            new_file_boxes = []
            new_scores = []
            for index, box, score in zip(top_box_indices, file_boxes, file_scores):
              boxes = box[index]
              scores = score[index]
              new_boxes = decode_box_coordinates(image, boxes)
              new_file_boxes.append(new_boxes)
              new_scores.append(scores)
            return new_file_boxes, new_scores
            '''
            file_boxes = file_boxes[top_box_indices]
            print(file_boxes)

            new_file_boxes = decode_box_coordinates(image, file_boxes)
            
            file_scores = file_scores[top_box_indices]
            print(file_scores)
            '''
            return new_file_boxes, file_scores
