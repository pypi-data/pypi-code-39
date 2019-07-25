import tensorflow as tf
import numpy as np

class RVQ(tf.keras.layers.Layer):
    def __init__(self, k, d, h, **kwargs):
        """
        :param k: number of vector in the code book
        :param d: dimension of vector
        :param h: num of heads
        """
        self.k = k
        self.d = d
        self.h = h
        m = np.log2(k)  # m bits
        assert m.is_integer()
        assert m//h == 0

        self.k_ = int(np.power(2, m//h))
        self.kernel = self.add_variable("kernel", shape=[h, self.k_, d//h])
        self.alpha = self.add_variable('alpha')

    def dist(self, input):
        repeats = [1] * input.shape.ndims
        repeats.insert(-1, self.h)
        repeats.insert(-1, self.k_)

        src = tf.expand_dims(input, -2)
        src = tf.expand_dims(src, -2)
        src = tf.tile(src, repeats)
        tgt = self.kernel
        for _ in repeats[0:-3]:
            tgt = tf.expand_dims(tgt, 0)
        d = tf.norm(src - tgt, axis=-1)
        return d

    def __call__(self, input):
        d = self.dist(input)  # [::, h, k_]
        ind = tf.argmin(d, -1)  # [::, h]
        v = tf.gather(self.kernel, ind)  # [::, h, d//h]
        shape = tf.shape(v)
        new_shape = tf.concat([shape[:-2], [self.d]], axis=0)
        v = tf.reshape(v, new_shape)
        v = self.alpha * input + (1 - self.alpha) * v
        base = tf.pow(self.k_, tf.range(h))
        ind *= base
        ind = tf.reduce_sum(ind, -1)
        return v, ind


class RVQA(tf.keras.Model):
    """
    residual vector quantized auto encoder
    paper: Unsupervised Paraphrasing without Translation https://arxiv.org/pdf/1905.12752.pdf

    """
    def __init__(self, k, d, encoder, decoder, **kwargs):
        """
        :param k: number of vector in the code book
        :param d: dimension of vector
        """
        self.vq = VQ(k, d)
        self.encoder = encoder
        self.decoder = decoder

        super(RVQA, self).__init__(**kwargs)


    def __call__(self, input):
        z_e = self.encoder(input)
        z_q, z_ind = self.vq(z_e)




