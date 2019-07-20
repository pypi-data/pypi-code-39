# -*- coding: utf-8 -*-
"""
module learner.py
--------------------
A base class definition for the learner class.
The default learner defines steps for the learning procedure.
"""
import tensorflow as tf
import numpy as np
from blinker import signal
import time


def initialize_session():
    """
    Runs the initializer for all not initialized variables in the default graph.
    """
    sess = tf.get_default_session()
    not_initialized = sess.run([tf.is_variable_initialized(var) for var in tf.global_variables()])
    not_initialized = [v for (v, f) in zip(tf.global_variables(), not_initialized) if not f]
    if len(not_initialized) > 0:
        sess.run(tf.variables_initializer(not_initialized))


def reinitialize_all_variables():
    """
    Runs the initializer for all variables in the default graph.
    """
    sess = tf.get_default_session()
    all_variables = [var for var in tf.global_variables()]
    if len(all_variables) > 0:
        sess.run(tf.variables_initializer(all_variables))


def partial_restore(save_path):
    """
    Restore all variables that are saved in the checkpoint and leave the variables that are not saved there unchanged.
    :param save_path: checkpoint path.
    """
    from tensorflow.python import pywrap_tensorflow

    reader = pywrap_tensorflow.NewCheckpointReader(save_path)
    var_to_shape_map = reader.get_variable_to_shape_map()
    all_vars = tf.global_variables()
    allvars_dic = dict()

    for var in all_vars:
        allvars_dic[var.name[:-2]] = var
    var_list = dict()
    for key in sorted(var_to_shape_map):
        var_list[key] = allvars_dic[key]

    sess = tf.get_default_session()
    saver = tf.train.Saver(var_list)
    saver.restore(sess, save_path)
