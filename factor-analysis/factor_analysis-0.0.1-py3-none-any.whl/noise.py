import tensorflow as tf

"""
This is the Noise object whose diagonal part is the noise vector
"""
class Noise():

    def __init__(self, factor, posterior):
        self.factor = factor
        self.posterior = posterior

    """
    Creates noise vector that is optimized
    """
    def create_noise(self, factor_):
        
        noise = 1/self.factor.data.shape[0].value * \
        (tf.matmul(tf.transpose(self.factor.data), self.factor.data) - \
        tf.reduce_sum(tf.matmul(tf.matmul(self.factor.data, tf.transpose(self.posterior.posterior_mean)), tf.transpose(factor_)), axis=0) - \
        tf.reduce_sum(tf.matmul(tf.matmul(factor_, self.posterior.posterior_mean), tf.transpose(self.factor.data)), axis=1) + \
        tf.reduce_sum(tf.matmul(tf.matmul(factor_, self.posterior.expectation_latent() + self.posterior.covariance_prior), 
        tf.transpose(factor_))))
        
        return tf.linalg.diag_part(noise)