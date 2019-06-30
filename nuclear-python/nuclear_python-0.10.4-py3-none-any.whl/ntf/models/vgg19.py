import tensorflow as tf
from .. import preprocess_imagenet
import os


__all__ = ['VGG19']


class VGG19:
    def __init__(self, x):
        h = preprocess_imagenet(x)
        self.preprocessed = h

        with tf.variable_scope('vgg19'):
            with tf.variable_scope('feature'):
                with tf.variable_scope('block1'):
                    h = tf.layers.conv2d(h, 64, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 64, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.max_pooling2d(h, 2, 2)

                with tf.variable_scope('block2'):
                    h = tf.layers.conv2d(h, 128, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 128, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.max_pooling2d(h, 2, 2)

                with tf.variable_scope('block3'):
                    h = tf.layers.conv2d(h, 256, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 256, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 256, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 256, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.max_pooling2d(h, 2, 2)

                with tf.variable_scope('block4'):
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.max_pooling2d(h, 2, 2)

                with tf.variable_scope('block5'):
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.conv2d(h, 512, 3, 1, activation=tf.nn.relu, padding='same')
                    h = tf.layers.max_pooling2d(h, 2, 2)

                self.feature = h
            with tf.variable_scope('avgpool'):
                pass

            with tf.variable_scope('classifier'):
                h = tf.transpose(h, [0, 3, 1, 2])
                h = tf.layers.flatten(h)
                self.pooled = h
                with tf.variable_scope('block1'):
                    h = tf.layers.dense(h, 4096, activation=tf.nn.relu)
                    h = tf.layers.dropout(h)

                with tf.variable_scope('block2'):
                    h = tf.layers.dense(h, 4096, activation=tf.nn.relu)
                    h = tf.layers.dropout(h)

                with tf.variable_scope('block3'):
                    self.logits = tf.layers.dense(h, 1000)

                self.probs = tf.nn.softmax(self.logits)

    def load(self, sess, ckpt_path):
        vs = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='vgg19')
        saver = tf.train.Saver(var_list=vs)
        saver.restore(sess, ckpt_path)

    def save(self, sess, ckpt_path):
        vs = tf.get_collection(tf.GraphKeys.TRAINABLE_VARIABLES, scope='vgg19')
        saver = tf.train.Saver(var_list=vs)
        os.makedirs(os.path.dirname(ckpt_path), exist_ok=True)
        saver.save(sess, ckpt_path)