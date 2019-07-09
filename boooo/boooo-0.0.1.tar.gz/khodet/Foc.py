import sys
import pkg_resources
import os
import tensorflow as tf

os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'
name = "Python" + str(sys.version_info[0]) + str(sys.version_info[1])
resource_package = name


def print_res():
    print(os.path.abspath("file4.txt"))
    print("Hey")
    file1 = open(os.path.abspath("file4.txt"), "r")
    sess = tf.compat.v1.Session()
    a = tf.constant(int(file1.readline(), 10))
    b = tf.constant(int(file1.readline(), 10))
    print(sess.run(a + b))


def print_the_other():
    sess = tf.compat.v1.Session()
    a = tf.constant(2)
    b = tf.constant(3)
    print(sess.run(a + b))


def print_it():
    print("hi")
    template = pkg_resources.resource_string(resource_package, 'file4.txt')
    print(template)




