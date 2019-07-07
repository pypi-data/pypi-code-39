# %%
import tensorflow as tf
from PIL import Image
import numpy as np
import json

# %%
# Load TFLite model and allocate tensors.
interpreter = tf.lite.Interpreter(model_path="models/facenet.tflite")
interpreter.allocate_tensors()
# Get input and output tensors.
input_details = interpreter.get_input_details()
output_details = interpreter.get_output_details()

# %%
img = Image.open('sample_inputs/dewald_profile.jpg')
img_160 = img.resize((160, 160), resample=Image.LANCZOS)
img_160.show()
img_160_arr = np.array(img_160)
input_data = np.expand_dims(img_160_arr, axis=0)
# %%
# Test model on random input data.
input_shape = input_details[0]['shape']
input_data = np.array(np.random.random_sample(input_shape), dtype=np.uint8)

# %%
interpreter.set_tensor(input_details[0]['index'], input_data)
interpreter.invoke()
output_data = interpreter.get_tensor(output_details[0]['index'])
print('INPUTS: ')
print(input_details)
print('OUTPUTS: ')
print(output_details)
print(json.dumps(output_data.tolist()[0]))
