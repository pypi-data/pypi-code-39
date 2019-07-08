import numpy as np
import tensorflow as tf

"""
This is the Factor object that deduces the factor of dimension: n x k
"""
class Factor():

    def __init__(self, data: np.array, posterior):
        self.data = tf.convert_to_tensor(data, dtype=tf.float64)
        self.posterior = posterior

    """
    Creates factor from data
    """
    def create_factor(self):
        mean = tf.reduce_mean(self.data, axis=0)
        
        series_factor = tf.reduce_sum(tf.multiply(
        tf.expand_dims(tf.subtract(self.data, mean), axis=2), 
        tf.transpose(self.posterior.posterior_mean)), axis=0)

        factor = tf.matmul(series_factor, tf.linalg.inv(self.posterior.expectation_latent()))
        
        return factor