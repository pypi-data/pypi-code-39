from torch import optim

from . import harness


class ReduceLROnPlateauCallback(harness.Callback):
    def __init__(self, optimizer, metric="val_loss", **kwargs):
        self.scheduler = optim.lr_scheduler.ReduceLROnPlateau(optimizer, **kwargs)
        self.metric = metric

    def on_epoch_end(self, harness, epoch, logs=None):
        logs = logs or {}
        metrics = logs["metrics"]
        self.scheduler.step(metrics[self.metric])


__all__ = ["ReduceLROnPlateauCallback"]
