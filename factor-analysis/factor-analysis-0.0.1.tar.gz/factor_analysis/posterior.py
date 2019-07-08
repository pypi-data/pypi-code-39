import numpy as np
import tensorflow as tf

"""
This is posterior object class which takes in μ and Σ from the latent conditional distribution.
"""
class Posterior(object):

    def __init__(self, covariance_prior: np.array, posterior_mean: np.array):
        self.covariance_prior = tf.convert_to_tensor(covariance_prior, dtype=tf.float64)
        self.posterior_mean = tf.convert_to_tensor(posterior_mean, dtype=tf.float64)

    """
    Expectation latent is the covariance component of the factor analysis
    """
    def expectation_latent(self) -> tf.Tensor:
        return tf.matmul(self.posterior_mean, tf.transpose(self.posterior_mean)) + self.covariance_prior

    """
    This is the actual mean of the latent components which can ve verified using the factor, noise and data
    """
    def verify_posterior_mean(self, factor: tf.Tensor, noise: tf.Tensor, data: tf.Tensor) -> tf.Tensor:
        mean = tf.reduce_mean(data, axis=0)
        factor_t = tf.transpose(factor)
        
        return tf.matmul(tf.matmul(factor_t, tf.linalg.inv(tf.matmul(factor, factor_t) + noise)), data - mean)
    
    """
    This is the actual covariance of the latent components which can be verified using the factor and noise
    """
    def verify_covariance_prior(self, factor: tf.Tensor, noise: tf.Tensor) -> tf.Tensor:
        factor_t = tf.transpose(factor)
        ones = tf.ones((factor.shape[1], factor.shape[1]))
        data_cov = tf.matmul(tf.matmul(factor_t, tf.linalg.inv(tf.matmul(factor, factor_t) + noise)), factor)
        
        return ones - data_cov