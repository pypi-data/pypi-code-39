import numpy as np
import tensorflow as tf
from tensorflow.keras.layers import Dense

from tf2rl.algos.policy_base import IRLPolicy
from tf2rl.algos.gail import GAIL, Discriminator
from tf2rl.networks.spectral_norm_dense import SNDense


class Normalizer():
    def __init__(self, num_inputs):
        self.n = tf.zeros(num_inputs)
        self.mean = tf.zeros(num_inputs)
        self.mean_diff = tf.zeros(num_inputs)
        self.var = tf.zeros(num_inputs)

    def observe(self, x):
        self.n += 1.
        last_mean = self.mean.clone()
        self.mean += (x-self.mean)/self.n
        self.mean_diff += (x-last_mean)*(x-self.mean)
        self.var = torch.clamp(self.mean_diff/self.n, min=1e-2)

    def normalize(self, inputs):
        obs_std = torch.sqrt(self.var)
        return (inputs - self.mean)/obs_std


class DiscriminatorWGAIL(Discriminator):
    def compute_reward(self, inputs):
        cur_rewards = -self.call(inputs)
        
        return rewards


class WGAIL(GAIL):
    def __init__(
            self,
            state_shape,
            action_dim,
            units=[32, 32],
            lr=0.001,
            enable_sn=False,
            enable_gp=True,
            enable_gc=False,
            name="WGAIL",
            **kwargs):
        """
        :param enable_sn (bool): If true, add spectral normalization in Dense layer
        :param enable_gp (bool): If true, add gradient penalty to loss function
        :param enable_gc (bool): If true, apply gradient clipping while training
        """
        assert enable_gp and enable_gc, \
            "You must choose either Gradient Penalty or Gradient Clipping." \
            "Both at the same time is not supported."
        IRLPolicy.__init__(
            self, name=name, **kwargs)
        self.disc = Discriminator(
            state_shape=state_shape, action_dim=action_dim,
            units=units, enable_sn=enable_sn, output_activation="linear")
        self.optimizer = tf.keras.optimizers.Adam(
            learning_rate=lr, beta_1=0.5)
        self._enable_gp = enable_gp
        self._enable_gc = enable_gc

    def train(self, agent_states, agent_acts, expert_states, expert_acts):
        loss, accuracy = self._train_body(agent_states, agent_acts,
                                          expert_states, expert_acts)
        tf.summary.scalar(name=self.policy_name+"/DiscriminatorLoss", data=loss)

    @tf.function
    def _train_body(self, agent_states, agent_acts, expert_states, expert_acts):
        epsilon = 1e-8
        with tf.device(self.device):
            with tf.GradientTape() as tape:
                real_logits = self.disc([expert_states, expert_acts])
                fake_logits = self.disc([agent_states, expert_acts])
                loss = -(tf.reduce_mean(real_logits) -
                         tf.reduce_mean(fake_logits))
            grads = tape.gradient(loss, self.disc.trainable_variables)
            self.optimizer.apply_gradients(
                zip(grads, self.disc.trainable_variables))

        return loss

    def inference(self, states, actions):
        if states.ndim == actions.ndim == 1:
            states = np.expand_dims(states, axis=0)
            actions = np.expand_dims(actions, axis=0)
        return self._inference_body(states, actions)

    @tf.function
    def _inference_body(self, states, actions):
        with tf.device(self.device):
            return tf.math.log(self.disc([states, actions]) + 1e-8)

    @staticmethod
    def get_argument(parser=None):
        import argparse
        if parser is None:
            parser = argparse.ArgumentParser(conflict_handler='resolve')
        parser.add_argument('--enable-sn', action='store_true')
        return parser
