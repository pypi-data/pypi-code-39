import os
import random

import torch
import numpy as np
from torch import nn
from visdom import Visdom

from .lr_scheduler import LinearLR4Finder
from .lr_scheduler import ExponentialLR4Finder


class AverageMeter(object):
    """Keeps track of most recent, average, sum, and count of a metric.

    Example
    -------
    losses = AverageMeter()
    losses.update(1, 5)
    print(losses.avg)
    """

    def __init__(self):
        self.reset()

    def reset(self):
        # Reset all value to 0.
        self.value = 0
        self.avg = 0
        self.sum = 0
        self.count = 0

    def update(self, value, n=1):
        """Update value, average, sum, and count.

        Parameters
        ----------
        n : int, optional (default = 5)
        value : double

        """
        self.value = value
        self.sum += value * n
        self.count += n
        self.avg = self.sum / self.count


class VisdomLinePlotter(object):
    """Plots lines in Visdom.

    Parameter
    ----------
    env_name: str, optional (default = 'main')
        Environment name of Visdom, you should not change it if don't know what's going on.

    Example
    -------
    import time

    plotter = VisdomLinePlotter()
    for x, y in zip(range(10), range(10)):
        plotter.plot("var_name", "split_name", "title_name", x, y)
        time.sleep(2)
    """

    def __init__(self, env_name="main"):
        self.viz = Visdom()
        self.env = env_name
        self.plots = {}

    def plot(self, var_name, split_name, title_name, x, y):
        if var_name not in self.plots:
            self.plots[var_name] = self.viz.line(
                X=np.array([x, x]),
                Y=np.array([y, y]),
                env=self.env,
                opts=dict(legend=[split_name], title=title_name, xlabel="Epochs", ylabel=var_name),
            )

        else:
            self.viz.line(
                X=np.array([x]),
                Y=np.array([y]),
                env=self.env,
                win=self.plots[var_name],
                name=split_name,
                update="append",
            )


def pytorch_reproducer(device="cpu", seed=2019):
    """Reproducer for pytorch experiment.

    Parameters
    ----------
    seed: int, optional (default = 2019)
    	Radnom seed.
    device: str, optinal (default = "cpu")
    	Device type.

    Example
    -------
    pytorch_reproducer(seed=2019, device=DEVICE).
    """
    torch.manual_seed(seed)
    np.random.seed(seed)
    random.seed(seed)
    if device == "cuda":
        torch.cuda.manual_seed(seed)
        torch.backends.cudnn.deterministic = True


def get_device():
    """Return device type.

    Return
    ------
    DEVICE: torch.device

    Example
    -------
    DEVICE = get_device()
    """
    DEVICE = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    return DEVICE


def clip_gradient(optimizer, grad_clip):
    """Clip gradients computed during backpropagation to prevent gradient explosion.

     Parameters
     ----------
     optimizer: pytorch optimizer
        Optimized with the gradients to be clipped.
     grad_clip: double
        Gradient clip value.

     Example
     -------
     from torch.optim import Adam
     from torchvision import models

     model = models.AlexNet()
     optimizer = Adam(model.parameters())
     clip_gradient(optimizer, 5)
     """
    # optimizer.param_groups is a list contain dict like below.
    # [{'amsgrad': False,'betas': (0.9, 0.999), 'eps': 1e-08, 'lr': 0.1, 'params': [tensor...]},
    # {'amsgrad': False,'betas': (0.9, 0.999), 'eps': 1e-08, 'lr': 0.1, 'params': [tensor...]}]
    for group in optimizer.param_groups:
        for param in group["params"]:
            if param.grad is not None:
                param.grad.data.clamp_(-grad_clip, grad_clip)


def init_conv2d(m):
    """Init parameters of convolution layer(初始化卷积层参数)

       Parameters
       ----------
       m: pytorch model

       Example
       -------
       class model(nn.Module):

           def __init__(self):
               super().__init__()

               # 初始化卷积层权重
               init_conv2d(self)
    """
    # 遍历网络子节点
    for c in m.modules():
        # 初始化卷积层
        if isinstance(c, nn.Conv2d):
            nn.init.xavier_uniform_(c.weight)
            nn.init.kaiming_normal_(c.weight, mode="fan_out", nonlinearity="relu")
            if c.bias is not None:
                nn.init.constant_(c.bias, 0.0)
        # 初始BatchNorm层
        elif isinstance(c, nn.BatchNorm2d):
            nn.init.constant_(c.weight, 1.0)
            nn.init.constant_(c.bias, 0.0)
        # 初始线性层
        elif isinstance(c, nn.Linear):
            nn.init.normal_(c.weight, 0.0, 0.01)
            nn.init.constant_(c.bias, 0.0)


def decimate(tensor, dims):
    """将tensor的维度变为dims
       Parameters
       ----------
       tensor: pytorch tensor
       dims: list

       Example
       -------
       x = torch.rand(4096, 512, 7, 7)
       decimate(x, [1024, None, 3, 3])
    """
    assert tensor.dim() == len(dims)

    for i in range(len(dims)):
        if dims[i] is not None:
            tensor = tensor.index_select(dim=i, index=torch.linspace(0, tensor.size()[i] - 1, dims[i]).long())

    return tensor


# ==============================================================================================================
# Learning rate related
# ==============================================================================================================
def adjust_learning_rate(optimizer, scale_factor):
    """Shrinks learning rate by a specified factor.

    Parameters
    ----------
    optimizer: pytorch optimizer
    scale_factor: factor to scale by
    """

    print("\nDECAYING learning rate.")
    for param_group in optimizer.param_groups:
        param_group["lr"] = param_group["lr"] * scale_factor
    print("The new learning rate is %f\n" % (optimizer.param_groups[0]["lr"],))


def get_learning_rate(optimizer):
    """Get learning rate.

    Parameters
    ----------
    optimizer: pytorch optimizer
    """
    lr = []
    for param_group in optimizer.param_groups:
        lr += [param_group["lr"]]

    assert len(lr) == 1  # we support only one param_group
    lr = lr[0]

    return lr


class LRFinder(object):
    def __init__(self, model, optimizer, criterion, device=None, memory_cache=True, cache_dir=None):
        self.model = model
        self.optimizer = optimizer
        self.criterion = criterion
        self.history = {"lr": [], "loss": []}
        self.best_loss = None
        self.memory_cache = memory_cache
        self.cache_dir = cache_dir

        # Save the original state of the model and optimizer so they can be restored if
        # needed
        self.model_device = next(self.model.parameters()).device
        self.state_cacher = StateCacher(memory_cache, cache_dir=cache_dir)
        self.state_cacher.store("model", self.model.state_dict())
        self.state_cacher.store("optimizer", self.optimizer.state_dict())

        # If device is None, use the same as the model
        if device:
            self.device = device
        else:
            self.device = self.model_device

    def reset(self):
        """Restores the model and optimizer to their initial states."""
        self.model.load_state_dict(self.state_cacher.retrieve("model"))
        self.optimizer.load_state_dict(self.state_cacher.retrieve("optimizer"))
        self.model.to(self.model_device)

    def range_test(
        self, train_loader, val_loader=None, end_lr=10, num_iter=100, step_mode="exp", smooth_f=0.05, diverge_th=5
    ):
        """Performs the learning rate range test.
        Arguments:
            train_loader (torch.utils.data.DataLoader): the training set data laoder.
            val_loader (torch.utils.data.DataLoader, optional): if `None` the range test
                will only use the training loss. When given a data loader, the model is
                evaluated after each iteration on that dataset and the evaluation loss
                is used. Note that in this mode the test takes significantly longer but
                generally produces more precise results. Default: None.
            end_lr (float, optional): the maximum learning rate to test. Default: 10.
            num_iter (int, optional): the number of iterations over which the test
                occurs. Default: 100.
            step_mode (str, optional): one of the available learning rate policies,
                linear or exponential ("linear", "exp"). Default: "exp".
            smooth_f (float, optional): the loss smoothing factor within the [0, 1[
                interval. Disabled if set to 0, otherwise the loss is smoothed using
                exponential smoothing. Default: 0.05.
            diverge_th (int, optional): the test is stopped when the loss surpasses the
                threshold:  diverge_th * best_loss. Default: 5.
        """
        # Reset test results
        self.history = {"lr": [], "loss": []}
        self.best_loss = None

        # Move the model to the proper device
        self.model.to(self.device)

        # Initialize the proper learning rate policy
        if step_mode.lower() == "exp":
            lr_schedule = ExponentialLR4Finder(self.optimizer, end_lr, num_iter)
        elif step_mode.lower() == "linear":
            lr_schedule = LinearLR4Finder(self.optimizer, end_lr, num_iter)
        else:
            raise ValueError("expected one of (exp, linear), got {}".format(step_mode))

        if smooth_f < 0 or smooth_f >= 1:
            raise ValueError("smooth_f is outside the range [0, 1[")

        # Create an iterator to get data batch by batch
        iterator = iter(train_loader)
        for iteration in tqdm(range(num_iter)):
            # Get a new set of inputs and labels
            try:
                inputs, labels = next(iterator)
            except StopIteration:
                iterator = iter(train_loader)
                inputs, labels = next(iterator)

            # Train on batch and retrieve loss
            loss = self._train_batch(inputs, labels)
            if val_loader:
                loss = self._validate(val_loader)

            # Update the learning rate
            lr_schedule.step()
            self.history["lr"].append(lr_schedule.get_lr()[0])

            # Track the best loss and smooth it if smooth_f is specified
            if iteration == 0:
                self.best_loss = loss
            else:
                if smooth_f > 0:
                    loss = smooth_f * loss + (1 - smooth_f) * self.history["loss"][-1]
                if loss < self.best_loss:
                    self.best_loss = loss

            # Check if the loss has diverged; if it has, stop the test
            self.history["loss"].append(loss)
            if loss > diverge_th * self.best_loss:
                print("Stopping early, the loss has diverged")
                break

        print("Learning rate search finished. See the graph with {finder_name}.plot()")


class StateCacher(object):
    def __init__(self, in_memory, cache_dir=None):
        self.in_memory = in_memory
        self.cache_dir = cache_dir

        if self.cache_dir is None:
            import tempfile

            self.cache_dir = tempfile.gettempdir()
        else:
            if not os.path.isdir(self.cache_dir):
                raise ValueError("Given `cache_dir` is not a valid directory.")

        self.cached = {}

    def store(self, key, state_dict):
        if self.in_memory:
            self.cached.update({key: copy.deepcopy(state_dict)})
        else:
            fn = os.path.join(self.cache_dir, "state_{}_{}.pt".format(key, id(self)))
            self.cached.update({key: fn})
            torch.save(state_dict, fn)

    def retrieve(self, key):
        if key not in self.cached:
            raise KeyError("Target {} was not cached.".format(key))

        if self.in_memory:
            return self.cached.get(key)
        else:
            fn = self.cached.get(key)
            if not os.path.exists(fn):
                raise RuntimeError("Failed to load state in {}. File does not exist anymore.".format(fn))
            state_dict = torch.load(fn, map_location=lambda storage, location: storage)
            return state_dict

    def __del__(self):
        """Check whether there are unused cached files existing in `cache_dir` before
        this instance being destroyed."""
        if self.in_memory:
            return

        for k in self.cached:
            if os.path.exists(self.cached[k]):
                os.remove(self.cached[k])
