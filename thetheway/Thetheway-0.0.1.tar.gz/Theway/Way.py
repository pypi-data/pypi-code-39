import sys
import pkg_resources
import os
import tensorflow as tf
os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

this_dir, this_filename = os.path.split(__file__)
DATA_PATH = os.path.join(this_dir, "Theway", "file6.txt")
# fullCorpus = pd.read_csv(DATA_PATH, sep="\t", header=None)
print(DATA_PATH)
print(this_dir)


def print_res():
    print("Hey")
    file1 = open(DATA_PATH, "r")
    sess = tf.compat.v1.Session()
    a = tf.constant(int(file1.readline(), 10))
    b = tf.constant(int(file1.readline(), 10))
    print(sess.run(a + b))


def print_the_other():
    sess = tf.compat.v1.Session()
    a = tf.constant(2)
    b = tf.constant(3)
    print(sess.run(a + b))

