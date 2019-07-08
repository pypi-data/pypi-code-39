from . import factors
from . import noise
from . import posterior
import tensorflow as tf

"""
The latent space can be obtained from this equation.
The latent space is of the dimension - m x k, or k x m, where
            m: data points, and 
            k: latent variables
            x = μ + Λz + ϵ
"""
def latent_space(data: tf.Tensor, factor: tf.Tensor, noise: tf.Tensor) -> tf.Tensor:
    s_t = tf.transpose(data)
    mean_s_t = tf.reduce_mean(s_t, axis=1)
    return tf.matmul(tfp.math.pinv(factor), 
        tf.subtract(tf.subtract(s_t, tf.expand_dims(mean_s_t, axis=1)), \
                tf.expand_dims(noise, axis=1)))