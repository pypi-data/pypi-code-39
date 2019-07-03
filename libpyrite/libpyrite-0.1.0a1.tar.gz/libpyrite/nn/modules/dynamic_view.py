from torch import nn


class DynamicView(nn.Module):
    def __init__(self, shape_fn):
        super(DynamicView, self).__init__()
        self.shape_fn = shape_fn

    def forward(self, x):
        return x.view(self.shape_fn(x))


__all__ = ["DynamicView"]
