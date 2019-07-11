from legos.callbacks import Callback
from legos.events import SkipEpochException


class SkipCallback(Callback):

    def __init__(self, batch_idx):
        self.batch_idx = batch_idx

    def batch_after(self):
        if self.learner.model.training:
            batch_idx = self.learner.batch_idx
            n_batches = self.learner.n_batches
            if batch_idx == self.batch_idx:
                print(f"TestCallback: SkipEpoch at {batch_idx + 1}/{n_batches}")
                raise SkipEpochException()
