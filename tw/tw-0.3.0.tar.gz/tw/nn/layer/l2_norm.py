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
"""FrozenBatchNorm2d"""
import torch
from torch import nn


class L2Norm(nn.Module):
  """ParseNet: Looking Wider to See Better -- used by SSD
    Normalize channels for the convolutional layer.
  """

  def __init__(self, n_dims, scale=20., eps=1e-10):
    super(L2Norm, self).__init__()
    self.n_dims = n_dims
    self.weight = nn.Parameter(torch.Tensor(self.n_dims))
    self.eps = eps
    self.scale = scale

  def forward(self, x):
    norm = x.pow(2).sum(1, keepdim=True).sqrt() + self.eps
    return self.weight[None, :, None, None].expand_as(x) * x / norm
