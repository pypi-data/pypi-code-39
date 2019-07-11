import torch
import matplotlib.pyplot as plt
from legos.callbacks import Callback
from legos.torch_utils import weighted_smooth


class RecorderStats():

    def __init__(self, metrics):
        '''
        Record all metrics value into a dictionary which used method.__name__ as key and a list as value to store the values.
        Args:
        metrics (list): a list of callable methods with the signature (pred, yb)
        '''
        self.metrics = metrics
        self.reset()

    def reset(self):
        self.stats = {m.__name__: [] for m in self.metrics }

    def add(self, learner):
        with torch.no_grad():
            for metric in self.metrics:
                key = metric.__name__
                value = learner.stats.current_stats.raw_stats[key].detach().cpu()
                self.stats[key].append(value)


class RecorderCallback(Callback):
    """
    Save raw metrics results from `StatsCallback` into a list so we can plot the history of each metrics.
    Therefore, this RecorderCallback need to have a larger `order` than `StatsCallback`
    """
    order = 10

    def __init__(self, metrics=[]):
        self.metrics = metrics
        self.train_stats, self.valid_stats = RecorderStats(metrics), RecorderStats(self.metrics)

    def fit_before(self):
        self.lrs = [[] for _ in self.learner.opt.param_groups]
        self.train_loss = []
        self.valid_loss = []
        self.train_stats.reset()
        self.valid_stats.reset()

    def record_training(self):
        if not self.learner.training: return

        for idx, pg in enumerate(self.learner.opt.param_groups):
            if 'lr' in pg:
                lr = pg['lr']
                self.lrs[idx].append(lr)

        self.train_loss.append(self.learner.loss.detach().cpu())
        self.train_stats.add(self.learner)

    def record_validation(self):
        self.valid_loss.append(self.learner.loss.detach().cpu())
        self.valid_stats.add(self.learner)

    def batch_after(self):
        if self.learner.training:
            self.record_training()
        else:
            self.record_validation()

    def plot_metric(self, metric_name, train=True, figsize=None, ax=None, label=True, smooth_weight=1.0):
        if ax is None: _, ax = plt.subplots(figsize=figsize)
        stats = self.train_stats.stats[metric_name] if train else self.valid_stats.stats[metric_name]
        ax.plot(weighted_smooth(stats, smooth_weight))
        if label:
            ax.set_title(f'{"Training" if train else "Validation"} {metric_name} per batch')
            ax.set_xlabel('batch index')
            ax.set_ylabel(f'{metric_name}')
        return ax

    def plot_metrics(self, figsize=(20, 5), axes=None, nrows=1, ncols=2, label=True, smooth_weight=0.5):
        nrows = len(self.metrics)
        if axes is None:
            _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
            axes = axes.flatten()
        for i, metric in enumerate(self.metrics):
            axes_idx = i * 2
            self.plot_metric(metric.__name__, train=True, ax=axes[axes_idx], figsize=figsize, label=label, smooth_weight=smooth_weight)
            axes_idx = i * 2 + 1
            self.plot_metric(metric.__name__, train=False, ax=axes[axes_idx], figsize=figsize, label=label, smooth_weight=smooth_weight)
        return axes

    def plot_lr(self, pg_id=-1, figsize=None, ax=None, label=True):
        if ax is None: _, ax = plt.subplots(figsize=figsize)
        ax.plot(self.lrs[pg_id])
        if label:
            ax.set_title('Learning rate per batch')
            ax.set_xlabel('batch index')
            ax.set_ylabel('lr')
        return ax

    def plot_loss(self, train=True, figsize=None, ax=None, label=True, smooth_weight=0.5):
        if ax is None: _, ax = plt.subplots(figsize=figsize)
        loss = self.train_loss if train else self.valid_loss
        ax.plot(weighted_smooth(loss, smooth_weight))
        if label:
            title = "Training" if train else "Validation"
            ax.set_title(f"{title} Loss per batch")
            ax.set_xlabel('batch index')
            ax.set_ylabel('loss')
        return ax

    def plot_losses(self, figsize=(20, 5), axes=None, nrows=1, ncols=2, label=True, smooth_weight=1.0):
        if axes is None: _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        self.plot_loss(train=True, ax=axes[0], label=label, smooth_weight=smooth_weight)
        self.plot_loss(train=False, ax=axes[1], label=label, smooth_weight=smooth_weight)
        return axes

    def plot_lr_loss(self, skip_last=0, pg_id=-1, label=True, ax=None, figsize=None):
        if ax is None: _, ax = plt.subplots(figsize=figsize)
        lr = self.lrs[pg_id]
        n = len(lr) - skip_last
        ax.set_xscale('log')
        ax.plot(lr[:n], self.train_loss[:n])
        if label:
            ax.set_title('Loss per lr')
            ax.set_xlabel('lr')
            ax.set_ylabel('loss')