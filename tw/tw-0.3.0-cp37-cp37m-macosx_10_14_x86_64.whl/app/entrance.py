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
"""Entrance: easy to custom"""
import argparse
from .defaults import _C


def dist_init(config, dist_device):
  """Distribution Configuration"""
  from . import dist

  # set basic information
  dist.init()
  config.DIST.RUN = True
  config.DIST.RANK = dist.rank()
  config.DIST.SIZE = dist.size()
  config.DIST.LOCAL_RANK = dist.local_rank()
  config.DIST.LOCAL_SIZE = dist.local_size()
  config.DIST.ROOT_RANK = 0
  config.DIST.IS_ROOT = config.DIST.RANK == config.DIST.ROOT_RANK

  # set device for each process
  if dist_device == 'cpu':
    devices = ['cpu' for i in range(config.DIST.LOCAL_SIZE)]
  elif dist_device == 'cuda':
    devices = ['cuda:%d' % i for i in range(config.DIST.LOCAL_SIZE)]
  else:
    devices = dist_device.split(',')
  config.INFO.DEVICE = devices[config.DIST.LOCAL_RANK]


def start(TARGETS):
  # parse command parameters
  parser = argparse.ArgumentParser()
  parser.add_argument('--config', type=str, dest='cfg', default=None,
                      help='Path to config.yaml file.')
  parser.add_argument('--task', type=str, dest='task', default=None,
                      help='Setting task type: train/test/val.')
  parser.add_argument('--device', type=str, dest='device', default=None,
                      help='Setting device type: cpu/cuda:0/cuda:1/.')
  parser.add_argument('--input', type=str, dest='input', default=None,
                      help='For inference, input test image/folder path.')
  parser.add_argument('--model', type=str, dest='model', default=None,
                      help='Setting the model.')
  parser.add_argument('--dir', type=str, dest='dir', default=None,
                      help='Setting output dir.')
  parser.add_argument('--dist', type=bool, default=False)
  parser.add_argument('--dist-device', type=str, default=None)
  args, _ = parser.parse_known_args()

  # mergin from config file
  _C.merge_from_file(args.cfg)

  # merging distribution
  if args.dist:
    dist_init(_C, args.dist_device)

  # Route Target
  if _C.INFO.TARGET in TARGETS:
    TARGETS[_C.INFO.TARGET](_C, **args.__dict__)
  else:
    raise ValueError(_C.INFO.TARGET.upper())
