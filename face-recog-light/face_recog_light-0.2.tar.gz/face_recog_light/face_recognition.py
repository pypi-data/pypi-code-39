"""
Largely based off of this script:
https://github.com/cmusatyalab/openface/blob/master/demos/sphere.py
"""
import os
import tensorflow as tf
from PIL import Image
import numpy as np
import json

MODEL_FILENAME = 'facenet.tflite'
MODELS_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), 'models'))

# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path=os.path.join(MODELS_DIR, MODEL_FILENAME))
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()


def encoding_from_image(aligned_face):

    img_160 = aligned_face.resize((160, 160), resample=Image.LANCZOS)
    img_160_arr = np.array(img_160)
    input_data = np.expand_dims(img_160_arr, axis=0)

    interpreter.set_tensor(input_details[0]['index'], input_data)
    interpreter.invoke()
    output_data = interpreter.get_tensor(output_details[0]['index'])
    return json.dumps(output_data.tolist()[0])
