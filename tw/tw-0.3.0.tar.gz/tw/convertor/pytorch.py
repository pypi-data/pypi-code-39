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
"""Exchange format with Convertor.
"""
from collections import OrderedDict
import numpy as np
from torch import nn
import flatbuffers
import tk


class Convertor():
  def __init__(self):
    self._buffer = None

  def create(self, name, params: nn.Module):
    assert self._buffer is None

    # model parameters
    params_ = params
    tensors_ = OrderedDict()
    builder = flatbuffers.Builder(0)

    # prepare data
    for key, value in params_.items():
      _name = builder.CreateString(key)
      _info = builder.CreateString("")
      tk.Tensor.TensorStartShapeVector(builder, len(list(value.shape)))
      for i in reversed(list(value.shape)):
        builder.PrependUint32(i)
      _shape = builder.EndVector(len(list(value.shape)))
      _size = np.prod(value.shape)
      _data = builder.CreateNumpyVector(value.contiguous().view(-1).numpy())
      tk.Tensor.TensorStart(builder)
      tk.Tensor.TensorAddName(builder, _name)
      tk.Tensor.TensorAddInfo(builder, _info)
      tk.Tensor.TensorAddSize(builder, _size)
      tk.Tensor.TensorAddShape(builder, _shape)
      tk.Tensor.TensorAddData(builder, _data)
      _tensor = tk.Tensor.TensorEnd(builder)
      tensors_[key] = _tensor
      print('[TensorKit] Added %s.' % key)

    tk.TensorMap.TensorMapStartTensorsVector(builder, len(tensors_))
    for key in reversed(tensors_):
      builder.PrependSOffsetTRelative(tensors_[key])
    _tensors = builder.EndVector(len(tensors_))

    # create a tensormap builder
    _name = builder.CreateString(name)
    _info = builder.CreateString("")
    tk.TensorMap.TensorMapStart(builder)
    tk.TensorMap.TensorMapAddName(builder, _name)
    tk.TensorMap.TensorMapAddInfo(builder, _info)
    tk.TensorMap.TensorMapAddTensors(builder, _tensors)
    tm = tk.TensorMap.TensorMapEnd(builder)
    builder.Finish(tm)
    print('[TensorKit] Successfully processed %s.' % key)
    self._buffer = builder.Output()
    return self

  def load(self, filepath):
    assert self._buffer is None
    with open(filepath, 'rb') as fp:
      self._buffer = fp.read()
    return self

  def dump(self, filepath):
    assert self._buffer is not None
    with open(filepath + '.twb', 'wb') as fw:
      fw.write(self._buffer)
    return self

  def view(self, params=None):
    """If pytorch model params are offered, it will automatically check values.
    """
    assert self._buffer is not None
    tm = tk.TensorMap.TensorMap.GetRootAsTensorMap(self._buffer, 0)
    print('[TensorKit] {:25} {:10} {:20} {:15} {:15} {:15} {:15} {:15}'.format(
        'NAME', 'SIZE', 'SHAPE', 'SUM', 'MAX', 'MIN', 'VAR', 'CHECK'))
    for i in range(tm.TensorsLength()):
      it = '[TensorKit] {:25} {:<10} {:20} {:<15f} {:<15f} {:<15f} {:<15f} {:<15}'
      shape = str([tm.Tensors(i).Shape(j)
                   for j in range(tm.Tensors(i).ShapeLength())])
      data = tm.Tensors(i).DataAsNumpy()
      name = tm.Tensors(i).Name().decode()
      size = tm.Tensors(i).Size()
      if params is None:
        check = 'None'
      elif abs(params[name].numpy().sum() - np.sum(data)) < 0.00001:
        check = 'True'
      else:
        check = 'False'
      it = it.format(name, size, shape, np.sum(data), np.max(
          data), np.min(data), np.var(data), check)
      print(it)
    return self
