import torch
import matplotlib.pyplot as plt
from torch import optim, nn
from torch.utils.data import DataLoader
from torchvision import datasets, transforms

from legos.torch_utils import get_device
from legos.datasets import DataBunch
from legos.events import (
    Events,
    SkipBackwardException,
    SkipBatchException,
    SkipEpochException,
    SkipOptimizerStepException,
    StopTrainException
)



class Learner():
    def __init__(self, model, optimizer, loss_func, data, callbacks=None, device=None):
        self.model: nn.Module = model
        self.opt: optim.Optimizer = optimizer
        self.loss_func = loss_func
        self.data: DataBunch = data
        self.device = device if device else get_device()
        self.callbacks = []
        self.add_cbs(callbacks)
        self.training = False

    def add_cbs(self, cbs):
        if not cbs: return
        for cb in cbs:
            self.add_cb(cb)

    def add_cb(self, cb):
        if not cb: return
        cb.learner = self
        setattr(self, cb.name, cb)
        self.callbacks.append(cb)

    def cb(self, event: Events):
        for cb in self.sorted_callbacks:
            func = getattr(cb, event.value, None)
            if func is not None:
                func()

    def backward_pass(self, loss):
        try:
            self.cb(Events.BACKWARD_BEFORE)
            self.loss.backward()

            self.cb(Events.OPTIM_STEP_BEFORE)
            self.opt.step()
            self.opt.zero_grad()
            self.cb(Events.OPTIM_STEP_AFTER)
        except SkipBackwardException:
            self.cb(Events.SKIP_BACKWARD)
        except SkipOptimizerStepException:
            self.cb(Events.SKIP_OPTIMIZER_STEP)
        finally:
            self.cb(Events.BACKWARD_AFTER)

    def one_batch(self, xb, yb):
        try:
            self.cb(Events.BATCH_BEFORE)
            self.xb, self.yb = xb.to(self.device), yb.to(self.device)
            self.pred = self.model(self.xb)
            self.loss = self.loss_func(self.pred, self.yb)

            if self.training:
                self.backward_pass(self.loss)
        except SkipBatchException:
            self.cb(Events.SKIP_BATCH)
        finally:
            self.cb(Events.BATCH_AFTER)

    def one_epoch(self, dataloader):
        try:
            self.n_batches = len(dataloader)
            self.cur_dl = dataloader
            self.cb(Events.EPOCH_BEFORE)
            for self.batch_idx, (xb, yb) in enumerate(dataloader):
                self.one_batch(xb, yb)
        except SkipEpochException:
            self.cb(Events.SKIP_EPOCH)
        finally:
            self.cb(Events.EPOCH_AFTER)

    def fit(self, n_epochs=1):
        try:
            self.n_epochs = n_epochs
            self.cb(Events.FIT_BEFORE)
            for self.epoch_idx in range(n_epochs):
                self.model.train()
                self.training = True
                self.one_epoch(self.data.train_dl)

                self.model.eval()
                self.training = False
                with torch.no_grad():
                    self.one_epoch(self.data.valid_dl)
        except StopTrainException:
            self.cb(Events.STOP_TRAIN)
        finally:
            self.cb(Events.FIT_AFTER)

    def lr_find(self, max_iter=100, min_lr=1e-6, max_lr=10, plot_results=True):
        '''
        Find the learning rate between `min_lr` and `max_lr` by
        changing the learning rate at every step and record the best loss.
        '''
        from legos.callbacks.lrfinder import LRFinderCallback
        from legos.callbacks.recorder import RecorderCallback

        old_callbacks = self.callbacks

        self.callbacks = []

        lr_finder_cb = LRFinderCallback(max_iter, min_lr, max_lr)
        self.add_cb(lr_finder_cb)

        if plot_results:
            self.add_cb(RecorderCallback())

        self.fit(n_epochs=max_iter)

        lr_finder_cb.summary()

        if plot_results:
            self.recorder.plot_lr()
            self.recorder.plot_lr_loss()

        # TODO: fit() method will change the parameters with the optimizer.step(). Need to revert this
        self.callbacks = []
        self.add_cbs(old_callbacks)

    @property
    def sorted_callbacks(self):
        return sorted(self.callbacks, key=lambda cb: cb.order)

    @property
    def batch_info(self):
        state = 'Train' if self.training else 'Valid'
        return f'Epoch [{self.epoch_idx + 1}/{self.n_epochs}] Batch [{self.batch_idx + 1}/{self.n_batches}] - {state} - '

    def get_lr(self, pg_id=-1):
        pg = self.opt.param_groups[pg_id]
        return pg.get('lr', None)

    def set_lr(self, lr, pg_id=-1):
        pg = self.opt.param_groups[pg_id]
        pg['lr'] = lr