import os
import tensorflow as tf


os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

file1 = open("file1.txt", "r")

sess = tf.compat.v1.Session()
a = tf.constant(int(file1.readline(), 10))
b = tf.constant(int(file1.readline(), 10))
print(sess.run(a + b))
