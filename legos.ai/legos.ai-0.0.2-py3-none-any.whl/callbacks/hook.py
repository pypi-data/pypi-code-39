import warnings
import torch
import math
import matplotlib.pyplot as plt
from functools import partial
from legos.callbacks import Callback
from legos.torch_utils import (
    get_module_names,
    get_named_modules_by_name,
)


def stats_hook(hook, module, input, output):
    if not module.training: return
    if not hasattr(hook,'means'): hook.means = []
    if not hasattr(hook,'stds'): hook.stds = []
    hook.means.append(output.data.mean().cpu())
    hook.stds.append(output.data.std().cpu())

def hists_hook(hook, module, input, output):
    if not module.training: return
    if not hasattr(hook,'hists'): hook.hists = []
    hook.hists.append(output.data.cpu().histc(40,0,10))

def plot_stats_hook(learner, module_names=[], axes=None, figsize=(20, 5), label=True):
    if len(module_names) == 0:
        module_names = learner.hook.module_names
    # plot forward
    ncols = 2 # one for mean, one for stds
    if learner.hook.forward and learner.hook.backward:
        nrows = 2
    else:
        nrows = 1

    if axes is None:
        _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.flatten()

    if learner.hook.forward:
        hooks = learner.hook.forward_hooks

        for i, name in enumerate(module_names):
            means, stds = hooks[name].means, hooks[name].stds
            axes[0].plot(means)
            axes[1].plot(stds)
        axes[0].legend(module_names)
        axes[1].legend(module_names)
        if label:
            axes[0].set_title('Mean of Training Output Activations')
            axes[0].set_xlabel('batch index')
            axes[0].set_ylabel('Mean')
            axes[1].set_title('Standard Deviation of Training Output Activations')
            axes[1].set_xlabel('batch index')
            axes[1].set_ylabel('Standard Deviation')

    if learner.hook.backward:
        raise NotImplementedError("do not support backward now.")
    return axes

def get_hist(h): return torch.stack(h).t().float().log1p()

def plot_hists_hook(learner, module_names=[], axes=None, ncols=2, figsize=(20, 5), label=True):
    if len(module_names) == 0:
        module_names = learner.hook.module_names
    if learner.hook.backward:
        raise NotImplementedError("do not support backward now.")

    nrows = math.ceil(len(module_names) / ncols)

    if axes is None:
        _, axes = plt.subplots(nrows=nrows, ncols=ncols, figsize=figsize)
        axes = axes.flatten()

    if learner.hook.forward:
        hooks = learner.hook.forward_hooks

        for i, name in enumerate(module_names):
            h = hooks[name].hists
            hist_img = get_hist(h)
            r, c = hist_img.shape
            axes[i].imshow(hist_img, origin='lower', aspect=c * 0.5/r)
            if label:
                axes[i].set_title(f'Histogram of Training Output Activations of {name}')
                axes[i].set_xlabel('batch index')
                axes[i].set_ylabel(f"{name}'s output")
    return axes


class Hook():
    def __init__(self, learner, module, funcs, is_forward):
        self.learner = learner
        if is_forward:
            self.hooks = [module.register_forward_hook(partial(func, self)) for func in funcs]
        else:
            self.hooks = [module.register_backward_hook(partial(func, self)) for func in funcs]

    def remove(self):
        for hook in self.hooks:
            hook.remove()

    def __del__(self): self.remove()

class HookCallback(Callback):

    def __init__(self, forward, backward, forward_hook_funcs=None, backward_hook_funcs=None, module_names=[]):
        '''
        Args:
        forward (bool): True if want to register forward hooks
        backward (bool): True if want to register backward hooks
        forward_hook_funcs (callback or list of callback): A function to process the forward hook. The signature should be function(hook, module, input, output) -> None
        forward_hook_funcs (callback or list of callback): A function to process the backward hook. The signature should be function(hook, module, grad_input, grad_output) -> Tensor or None
        module_names (list of str): a list of module to hook. Get all available hooks with method `get_module_names(model)`.
        '''
        if backward:
            raise NotImplementedError("do not support backward now. Check: https://github.com/pytorch/pytorch/issues/12331")

        if not forward and not backward:
            warnings.warn(f"{self.__class__.__name__} should has at least forward or backward enable!")

        if forward and forward_hook_funcs is None:
            raise ValueError("forward is enabled but forward_hook_funcs is None")

        if backward and backward_hook_funcs is None:
            raise ValueError("backward is enabled but backward_hook_funcs is None")

        self.forward, self.backward = forward, backward
        self.forward_hook_funcs = forward_hook_funcs if type(forward_hook_funcs) is list else [forward_hook_funcs]
        self.backward_hook_funcs = backward_hook_funcs if type(backward_hook_funcs) is list else [backward_hook_funcs]

        self.module_names = module_names

    def fit_before(self):
        if len(self.module_names) == 0:
            self.module_names = get_module_names(self.learner.model)
        self.modules = get_named_modules_by_name(self.learner.model, self.module_names)
        self.forward_hooks = self.backward_hooks = None
        if self.forward:
            self.forward_hooks = {name: Hook(self.learner, module, self.forward_hook_funcs, True) for name, module in self.modules}
        if self.backward:
            self.backward_hooks = {name: Hook(self.learner, module, self.backward_hook_funcs, False) for name, module in self.modules}

    def fit_after(self):
        if self.forward_hooks:
            for h in self.forward_hooks.values():
                h.remove()
        if self.backward_hooks:
            for h in self.backward_hooks.values():
                h.remove()
