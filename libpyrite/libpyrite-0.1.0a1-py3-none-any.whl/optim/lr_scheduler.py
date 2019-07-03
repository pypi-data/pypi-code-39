from abc import ABC, abstractmethod
import math

from torch.optim import Optimizer


class AbstractLRScheduler(ABC):
    """Abstract learning rate scheduling class.

    Changes the learning rate of the parameters groups for a given `Optimizer`. This learning
    rate scheduler operates on the more generic concept of iterations, as oppposed to epochs. This
    enable subclasses to be stepped at arbitrary time frames, such as batches.

    Subclasses must implement the `get_lr` method.
    """

    def __init__(self, optimizer):
        if not isinstance(optimizer, Optimizer):
            raise TypeError("{} is not an Optimizer".format(type(optimizer).__name__))
        self.optimizer = optimizer
        for group in optimizer.param_groups:
            if "initial_lr" not in group:
                group.setdefault("initial_lr", group["lr"])
        self.base_lrs = list(
            map(lambda group: group["initial_lr"], optimizer.param_groups)
        )
        self.last_iteration = -1

    def state_dict(self):
        """Return the state of the scheduler as a `dict`.

        It contains an entry for every variable in self.__dict__ which is not the optimizer.

        Returns:
            dict: the state dict.
        """
        return {
            key: value for key, value in self.__dict__.items() if key != "optimizer"
        }

    def load_state_dict(self, state_dict):
        """Load the scheduler's state.

        Arguments:
            state_dict (dict): Scheduler state. Should be an object returned
                from a call to `state_dict`.
        """
        self.__dict__.update(state_dict)

    @abstractmethod
    def get_lr(self):
        """Return the current learning rate for each parameter group.

        This is an abstract method, and as such, subclasses must implement it.

        Returns:
            List[float]: list of current learning rates.
        """
        raise NotImplementedError

    def step(self, iteration=None):
        """Step the scheduler, updating the learning rates for each parameter group."""
        if iteration is None:
            iteration = self.last_iteration + 1
        self.last_iteration = iteration
        for param_group, lr in zip(self.optimizer.param_groups, self.get_lr()):
            param_group["lr"] = lr


class TriangularCLR(AbstractLRScheduler):
    def __init__(self, optimizer, base_lr, max_lr, stepsize, last_iteration=-1):
        if base_lr >= max_lr:
            raise ValueError(
                "base_lr must be strictly less than max_lr ({} >= {})".format(
                    base_lr, max_lr
                )
            )
        if stepsize <= 0:
            raise ValueError("stepsize must be greater than zero ({})".format(stepsize))

        super(TriangularCLR, self).__init__(optimizer)
        self.base_lr = base_lr
        self.max_lr = max_lr
        self.stepsize = stepsize

    def get_lr(self):
        cycle = math.floor(1 + self.last_iteration / (2 * self.stepsize))
        x = abs(self.last_iteration / self.stepsize - 2 * cycle + 1)
        lr = self.base_lr + (self.max_lr - self.base_lr) * max(0, (1 - x))

        return [lr] * len(self.optimizer.param_groups)


__all__ = ["AbstractLRScheduler", "TriangularCLR"]
