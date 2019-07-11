from legos.callbacks import Callback


class LoggerCallback(Callback):
    """
    LoggerCallback will print the loss in `Learner` and metrics in `StatsCallback` into console.
    Therefore, the `order` should be larger than `StatsCallback`.
    """

    order = 10

    def __init__(self, metrics=[]):
        self.metrics = metrics

    def batch_after(self):
        batch_idx = self.learner.batch_idx
        epoch_idx = self.learner.epoch_idx
        n_epochs = self.learner.n_epochs
        n_batches = self.learner.n_batches
        if batch_idx % 200 == 0 or batch_idx == n_batches - 1:
            loss = self.learner.loss.item()
            metrics = self.metrics_summary()
            print(f"{self.learner.batch_info} Loss = {loss} {metrics}")

    def metrics_summary(self):
        outputs = ''
        for metric in self.metrics:
            key = metric.__name__
            outputs += f'- {key} = {self.learner.stats.current_stats[key]} '
        return outputs