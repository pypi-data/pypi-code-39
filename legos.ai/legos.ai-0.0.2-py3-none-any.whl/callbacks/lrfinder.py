from legos.callbacks import Callback
from legos.callbacks.schedulers import exp_func
from legos.events import StopTrainException


class LRFinderCallback(Callback):

    def __init__(self, max_iter, min_lr, max_lr, sched_func=None, pg_id=-1):
        self.max_iter = max_iter
        self.min_lr, self.max_lr = min_lr, max_lr
        self.pg_id = pg_id
        self.sched_func = exp_func(min_lr, max_lr) if sched_func is None else sched_func

    def summary(self):
        print(f'best loss = {self.best_loss} with lr = {self.best_lr} at iter = {self.best_iter}')

    def fit_before(self):
        self.cur_iter = 0
        self.best_loss = 1e9
        self.best_lr = None
        self.best_iter = None

    def batch_before(self):
        pos = self.cur_iter * 1.0 / self.max_iter
        self.learner.set_lr(self.sched_func(pos))

    def batch_after(self):
        loss = self.learner.loss.detach().cpu()
        if loss < self.best_loss:
            self.best_loss = loss
            self.best_lr = self.learner.get_lr(self.pg_id)
            self.best_iter = self.cur_iter

        self.cur_iter += 1
        if self.cur_iter > self.max_iter:
            raise StopTrainException()
