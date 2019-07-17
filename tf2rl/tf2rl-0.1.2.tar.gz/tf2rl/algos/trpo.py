import numpy as np
import tensorflow as tf

from tf2rl.algos.vpg import VPG


class TRPO(VPG):
    def __init__(
            self,
            backtrack_iters=10,
            backtrack_coef=0.8,
            damping_coef=0.1,
            name="PPO",
            **kwargs):
        kwargs["hidden_activation"] = "tanh"
        super().__init__(name=name, **kwargs)
        self._backtrace_iters = backtrack_iters
        self._backtrace_coef = backtrack_coef
        self._damping_coef = damping_coef

    def train(self, states, actions, advantages, logp_olds, returns):
        self._train_actor_body(states, actions, advantages, logp_olds)

    def _train_actor_body(self, states, actions, advantages, logp_olds):
        with tf.device(self.device):
            with tf.GradientTape() as tape:
                logp_news = self.actor.compute_log_probs(
                    states, actions)
                ratio = tf.math.exp(
                    logp_news - tf.squeeze(logp_olds))
                weights = tf.stop_gradient(tf.squeeze(advantages))
                actor_loss = -tf.reduce_mean(ratio * weights)
            actor_grads = tape.gradient(
                actor_loss, self.actor.trainable_variables)
            kl = sel
            tf.gradients(xs=params, ys=f)
            tf.concat([tf.reshape(x,(-1,)) for x in xs], axis=0)