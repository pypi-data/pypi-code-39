import torch
import math
import matplotlib.pyplot as plt
from functools import partial
from legos.callbacks import Callback


def sched_func(f):
    def _inner(start, end):
        return partial(f, start, end)
    return _inner

@sched_func
def linear_func(start, end, pos):
    return start + pos * (end - start)

@sched_func
def exp_func(start, end, pos):
    return start * (end / start) ** pos

@sched_func
def cos_func(start, end, pos):
    return start + (1 + math.cos(math.pi*(1-pos))) * (end-start) / 2

def combine_sched(percentages, list_funcs):
    assert sum(percentages) == 1
    assert len(percentages) == len(list_funcs)
    pcts = torch.tensor([0] + percentages)
    assert torch.all(pcts >= 0)
    pcts = torch.cumsum(pcts, 0)
    n_funcs = len(list_funcs)

    def combined(pos):
        sched_idx = (pos >= pcts).nonzero().max()
        sched_idx = min(sched_idx, n_funcs - 1)
        func = list_funcs[sched_idx]
        sched_pos = (pos - pcts[sched_idx]) / (pcts[sched_idx + 1] - pcts[sched_idx])
        return func(sched_pos)
    return combined

def plot_sched(f):
    outputs = [f(pos * 0.01) for pos in range(0, 100)]
    plt.plot(outputs)


class ParamSchedulerCallback(Callback):
    '''
    Schedule any hyperparameters that are registerd in optimizer param groups
    '''
    def __init__(self, param_func_dict, on_epoch=True):
        '''
        Args:
        param_func_dict (dict): a dictionary of parameter name and the function to schedule that parameter.
        on_epoch (bool): True if the position is calculated using epoch position. False if using batch position. Default: True
        '''
        self.param_func_dict = param_func_dict
        self.on_epoch = on_epoch

    def epoch_before(self):
        if self.on_epoch:
            pos = self.learner.epoch_idx / self.learner.n_epochs
            self.update_param(pos)

    def batch_before(self):
        if not self.on_epoch:
            pos = self.learner.batch_idx / self.learner.n_batches
            self.update_param(pos)

    def update_param(self, pos):
        '''
        Update the parameter for each param groups in the Optimizer
        '''
        for name, func in self.param_func_dict.items():
            for pg in self.learner.opt.param_groups:
                if name in pg:
                    pg[name] = func(pos)