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
"""Test for RNN"""
import torch
from torch import nn
from torch.nn import functional as F
import rnn


class SeqNet(nn.Module):
  def __init__(self):
    super(SeqNet, self).__init__()
    self.rnn2 = rnn.LSTM(1024, 256, 3, bias=True, batch_first=True)
    nn.init.constant_(self.rnn2.weight_ih_l0, 0.01)
    nn.init.constant_(self.rnn2.weight_hh_l0, 0.1)
    nn.init.constant_(self.rnn2.bias_ih_l0, 0.1)
    nn.init.constant_(self.rnn2.bias_hh_l0, 1.0)
    nn.init.constant_(self.rnn2.weight_ih_l1, 0.01)
    nn.init.constant_(self.rnn2.weight_hh_l1, 0.1)
    nn.init.constant_(self.rnn2.bias_ih_l1, 0.1)
    nn.init.constant_(self.rnn2.bias_hh_l1, 1.0)
    nn.init.constant_(self.rnn2.weight_ih_l2, 0.01)
    nn.init.constant_(self.rnn2.weight_hh_l2, 0.1)
    nn.init.constant_(self.rnn2.bias_ih_l2, 0.1)
    nn.init.constant_(self.rnn2.bias_hh_l2, 1.0)

    self.rnn3 = nn.LSTM(1024, 256, 3, bias=True, batch_first=True)
    for k, v in self.rnn3.state_dict().items():
      print('rnn3: ', k, v.shape)
    nn.init.constant_(self.rnn3.weight_ih_l0, 0.01)
    nn.init.constant_(self.rnn3.weight_hh_l0, 0.1)
    nn.init.constant_(self.rnn3.bias_ih_l0, 0.1)
    nn.init.constant_(self.rnn3.bias_hh_l0, 1.0)
    nn.init.constant_(self.rnn3.weight_ih_l1, 0.01)
    nn.init.constant_(self.rnn3.weight_hh_l1, 0.1)
    nn.init.constant_(self.rnn3.bias_ih_l1, 0.1)
    nn.init.constant_(self.rnn3.bias_hh_l1, 1.0)
    nn.init.constant_(self.rnn3.weight_ih_l2, 0.01)
    nn.init.constant_(self.rnn3.weight_hh_l2, 0.1)
    nn.init.constant_(self.rnn3.bias_ih_l2, 0.1)
    nn.init.constant_(self.rnn3.bias_hh_l2, 1.0)

  def forward(self, x):
    """x is a 3-d tensor: a batch (n, depth, ch)"""
    output, (state, cell) = self.rnn2(x)
    print('state', state.shape)
    print(output.shape)
    output = torch.sum(output, dim=2)
    print(output.sum(), state.sum())

    output, (state, cell) = self.rnn3(x)
    print('state', state.shape)
    print(output.shape)
    output = torch.sum(output, dim=2)
    print(output.sum(), state.sum())

    return output


def run():
  model = SeqNet()
  x = torch.rand(8, 16, 1024)
  with torch.no_grad():
    out = model.forward(x)


if __name__ == "__main__":
  run()
