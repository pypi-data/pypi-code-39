import numpy as np
import tensorflow as tf

from tf2rl.algos.vpg import VPG


def cg(Ax, b):
    """
    Conjugate gradient algorithm
    (see https://en.wikipedia.org/wiki/Conjugate_gradient_method)
    """
    x = np.zeros_like(b)
    r = b.copy() # Note: should be 'b - Ax(x)', but for x=0, Ax(x)=0. Change if doing warm start.
    p = r.copy()
    r_dot_old = np.dot(r,r)
    for _ in range(cg_iters):
        z = Ax(p)
        alpha = r_dot_old / (np.dot(p, z) + EPS)
        x += alpha * p
        r -= alpha * z
        r_dot_new = np.dot(r,r)
        p = r + (r_dot_new / r_dot_old) * p
        r_dot_old = r_dot_new
    return x


class TRPOTRPO(VPG):
    def __init__(
            self,
            clip=True,
            clip_ratio=0.2,
            name="PPO",
            **kwargs):
        super().__init__(name=name, **kwargs)
        self.clip = clip
        self.clip_ratio = clip_ratio

    def train_actor(self, states, actions, advantages, logp_olds):
        # Normalize advantages
        if self.normalize_adv:
            advantages = (advantages - np.mean(advantages)) / np.std(advantages)

        actor_loss, logp_news, ratio = self._train_actor_body(
            states, actions, advantages, logp_olds)
        return actor_loss

    @tf.function
    def _train_actor_body(self, states, actions, advantages, logp_olds):
        with tf.device(self.device):
            # Update actor
            with tf.GradientTape() as tape:
                logp_news = self.actor.compute_log_probs(states, actions)
                actor_loss = tf.reduce_mean(surr_loss)  # + lambda * entropy
            actor_grad = tape.gradient(
                actor_loss, self.actor.trainable_variables)
            self.actor_optimizer.apply_gradients(
                zip(actor_grad, self.actor.trainable_variables))

        return actor_loss, logp_news, ratio
