# Copyright 2018 The KaiJIN Authors. All Rights Reserved.
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# ==============================================================================
"""Solver
 1) optimizer
 2) lr_scheduler

Usage:
  solver = Solver()
  solver.SetOptim..()
  solver.SetLR..()

Method:
  solver.optimizer
  solver.lr
  solver.CurrentLR()
"""
import torch.optim
from .warmup_multistep_lr import WarmupMultiStepLR
from ..app import dist


class Solver():
  def __init__(self):
    self._optimizer = None
    self._lr = None
    self._params_group = []

  @property
  def optimizer(self):
    assert self._optimizer is not None
    return self._optimizer

  @property
  def lr(self):
    assert self._lr is not None
    return self._lr

  def CurrentLR(self):
    assert self._optimizer is not None
    return self._optimizer.param_groups[0]['lr']

  def SetDistributedOptimizer(self, named_params):
    """Binding distributed solver to params"""
    self._optimizer = dist.DistributedOptimizer(
        optimizer=self._optimizer,
        named_parameters=named_params)
    return self

  def SetOptimAdam(self,
                   params,
                   base_lr=1e-3,
                   betas=(0.9, 0.999),
                   eps=1e-8,
                   weight_decay=0.0):
    assert self._optimizer is None
    self._optimizer = torch.optim.Adam(
        params,
        lr=base_lr,
        betas=betas,
        eps=eps,
        weight_decay=weight_decay,
        amsgrad=False)
    return self

  def SetOptimAMSGrad(self,
                      params,
                      base_lr=1e-3,
                      betas=(0.9, 0.999),
                      eps=1e-8,
                      weight_decay=0.0):
    assert self._optimizer is None
    self._optimizer = torch.optim.Adam(
        params,
        lr=base_lr,
        betas=betas,
        eps=eps,
        weight_decay=weight_decay,
        amsgrad=True)
    return self

  def SetOptimSGD(self,
                  params,
                  base_lr=0.01,
                  momentum=0.9,
                  weight_decay=0.000):
    # if has configured
    assert self._optimizer is None
    self._optimizer = torch.optim.SGD(
        params,
        lr=base_lr,
        momentum=momentum,
        weight_decay=weight_decay)
    return self

  def SetLRWarmupMultiStep(self,
                           steps,
                           gamma=0.1,
                           warmup_factor=1.0/3,
                           warmup_iters=500,
                           warmup_method='linear',
                           last_epoch=-1):
    # if has configured
    assert self._lr is None
    assert self._optimizer is not None
    self._lr = WarmupMultiStepLR(
        self._optimizer,
        steps,
        gamma=gamma,
        warmup_factor=warmup_factor,
        warmup_iters=warmup_iters,
        warmup_method=warmup_method,
        last_epoch=last_epoch)
    return self

  def SetLRConstant(self):
    assert self._lr is None
    assert self._optimizer is not None
    self._lr = torch.optim.lr_scheduler.LambdaLR(
        self._optimizer,
        lr_lambda=lambda epoch: 1,
        last_epoch=-1)
    return self

  def SetLRMultiStep(self,
                     steps,
                     gamma=0.1,
                     last_epoch=-1):
    assert self._lr is None
    assert self._optimizer is not None
    self._lr = torch.optim.lr_scheduler.MultiStepLR(
        self._optimizer,
        steps,
        gamma=gamma,
        last_epoch=last_epoch)
    return self

  def AddRegularizationL1(self,
                          params,
                          weight_decay):
    assert self._optimizer is not None
    return weight_decay * sum(v.data.sum() for v in params)

  def AddRegularizationL2(self,
                          params,
                          weight_decay):
    assert self._optimizer is not None
    return weight_decay * sum(v.data.pow(2).sum() for v in params)
