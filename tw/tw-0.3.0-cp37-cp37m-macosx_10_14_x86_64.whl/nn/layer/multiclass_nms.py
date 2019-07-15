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
"""Multiclass-NMS ops"""
import torch
from .nms import NonMaxSuppression


class MulticlassNMS(torch.nn.Module):
  def __init__(self, nms_type='nms'):
    super(MulticlassNMS, self).__init__()
    if nms_type == 'nms':
      self.nms = NonMaxSuppression()
    else:
      raise NotImplementedError

  def forward(self,
              bboxes,
              scores,
              conf_thresh,
              nms_thresh,
              max_instances=0):
    """NMS for multiclass bboxes

    Args:
      bboxes (Tensor): [N, 4]
      scores (Tensor): [N, num_classes]
      conf_thresh (float): bboxes with scores lower will not be considered.
      nms_thresh (float): higher the thresh will be merged.

    Returns:
      tuple: (bboxes, labels): tensors of shape (k, 5) and (k, 1).
    """
    num_classes = scores.size(1)
    preds = []
    labels = []

    # assuming 0 is the background
    # indepdently processing for each classification
    for i in range(1, num_classes):
      cls_inds = scores[:, i] > conf_thresh
      if not cls_inds.any():
        continue
      bbox = bboxes[cls_inds, :]  # [M, 4]
      score = scores[cls_inds, i]  # [M]
      pred = torch.cat([bbox, score[:, None]], dim=1)  # [M, 5]
      pred, _ = self.nms(pred, nms_thresh)
      label = bboxes.new_full((pred.shape[0], ), i - 1, dtype=torch.long)
      labels.append(label)
      preds.append(pred)

    # merging
    if preds:
      preds, labels = torch.cat(preds), torch.cat(labels)
      if max_instances > 0:
        # last value represent score
        _, inds = preds[:, -1].sort(descending=True)
        inds = inds[:max_instances]
        preds = preds[inds]
        labels = labels[inds]
    else:
      preds = bboxes.new_zeros((0, 5))
      labels = bboxes.new_zeros((0, ), dtype=torch.long)

    return preds, labels
