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
"""nn"""
# cuda/csrc
from .layer.nms import NonMaxSuppression
from .layer.multiclass_nms import MulticlassNMS
from .layer.roi_align import RoIAlign
from .layer.roi_pool import ROIPool

# python
from .layer.frozen_batch_norm import FrozenBatchNorm2D

# Empty layer
from .layer.empty_op import EmptyBatchNorm2d
from .layer.empty_op import EmptyConv2d
from .layer.empty_op import EmptyConvTranspose2d
from .layer.empty_op import EmptyInterpolate
from .layer.empty_op import EmptyLayer

# Normalization
from .layer.l2_norm import L2Norm

# detection layer
from .layer.yolo_layer import YOLOLayer

# rnn
from .layer.rnn import RNN
from .layer.rnn import GRU
from .layer.rnn import LSTM

# loss
from .layer.sigmoid_focal_loss import SigmoidFocalLoss
from .loss.smooth_l1_loss import SmoothL1Loss

# metric
from .metric.regression import RegressionMetric
from .metric.top_k import TopkMetric


__all__ = [
    'NonMaxSuppression',
    'MulticlassNMS',
    'RoIAlign',
    'ROIPool',
    'FrozenBatchNorm2D',
    'EmptyBatchNorm2d',
    'EmptyConv2d',
    'EmptyConvTranspose2d',
    'EmptyInterpolate',
    'EmptyLayer',
    'YOLOLayer',
    'SmoothL1Loss',
    'SigmoidFocalLoss',
    'RegressionMetric',
    'TopkMetric',
    'L2Norm'
]
