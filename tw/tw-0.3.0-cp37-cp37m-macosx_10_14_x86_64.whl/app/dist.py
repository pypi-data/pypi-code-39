# Copyright 2017 The KaiJIN Authors. All Rights Reserved.
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
"""Distribution Wrapper"""
import torch
import horovod.torch as hvd
from horovod.torch.compression import Compression


def init():
  hvd.init()


def allgather(tensor, name=None):
  return hvd.allgather(tensor, name)


def allreduce(tensor, average=True, name=None):
  return hvd.allreduce(tensor, average, name)


def allreduce_scalr(scalr, average=True, name=None):
  return allreduce(torch.tensor(scalr), average, name).item()


def DistributedOptimizer(optimizer,
                         named_parameters=None,
                         compression=Compression.none,
                         backward_passes_per_step=1):
  return hvd.DistributedOptimizer(optimizer,
                                  named_parameters,
                                  compression,
                                  backward_passes_per_step)


def broadcast(tensor, root_rank, name=None):
  return hvd.broadcast(tensor, root_rank, name)


def broadcast_parameters(params, root_rank):
  return hvd.broadcast_parameters(params, root_rank)


def local_rank():
  return hvd.local_rank()


def local_size():
  return hvd.local_size()


def rank():
  return hvd.rank()


def size():
  return hvd.size()
