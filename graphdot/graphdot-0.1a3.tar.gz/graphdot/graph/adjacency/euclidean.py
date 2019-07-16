#!/usr/bin/env python
# -*- coding: utf-8 -*-
"""
Convert spatial distances between nodes to edge adjacencies
"""
import numpy as np


class Gaussian:
    def __init__(self, length_scale):
        self.length_scale = length_scale

    def __call__(self, x, y):
        return np.exp(-0.5 * np.sum((x - y)**2) / self.length_scale**2)


class Tent:
    def __init__(self, cutoff, order):
        self.cutoff = cutoff
        self.order = order

    def __call__(self, x, y):
        h = 1 - np.linalg.norm(x - y) / self.cutoff
        return h**self.order if h >= 0 else 0
