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
"""A basic configuration
"""
from yacs.config import CfgNode as CN
import socket

# -------------------------------------------------------------------------------
# Basic Information
# -------------------------------------------------------------------------------
_C = CN(new_allowed=True)
_C.INFO = CN(new_allowed=True)
_C.INFO.NAME = 'default'
_C.INFO.TASK = 'train'
_C.INFO.DIR = None
_C.INFO.OUTPUTS = '_outputs/'
_C.INFO.TARGET = None
_C.INFO.DEVICE = 'cpu'

# -------------------------------------------------------------------------------
# Distributed Configuration
# -------------------------------------------------------------------------------
_C.DIST = CN(new_allowed=True)
_C.DIST.RUN = False
_C.DIST.IP = socket.gethostbyname(socket.gethostname())
_C.DIST.HOSTNAME = socket.gethostname()
_C.DIST.IS_ROOT = True
_C.DIST.ROOT_RANK = 0  # dist root rank
_C.DIST.RANK = 0  # global rank
_C.DIST.SIZE = 1  # global size
_C.DIST.LOCAL_RANK = 0  # local rank
_C.DIST.LOCAL_SIZE = 1  # local size

# -------------------------------------------------------------------------------
# Log Configuration
# -------------------------------------------------------------------------------
_C.LOG = CN(new_allowed=True)
_C.LOG.STOP = None
_C.LOG.PRINT = 20
_C.LOG.SAVE = 1000
_C.LOG.TEST = None
_C.LOG.VAL = None

# -------------------------------------------------------------------------------
# Model Related Info
# -------------------------------------------------------------------------------
_C.MODEL = CN(new_allowed=True)
_C.MODEL.WEIGHT = None
_C.MODEL.ARCH = None
_C.MODEL.BACKBONE = None

# -------------------------------------------------------------------------------
# Datasets
# -------------------------------------------------------------------------------
_C.DATASET = CN(new_allowed=True)
_C.DATASET.INFO = CN(new_allowed=True)
_C.DATASET.INFO.NAME = None

# -------------------------------------------------------------------------------
# Solver
# -------------------------------------------------------------------------------
_C.SOLVER = CN()
_C.SOLVER.OPTIM = CN(new_allowed=True)
_C.SOLVER.OPTIM.METHOD = 'sgd'
_C.SOLVER.OPTIM.WD = 0.0000

# LEARNING RATE
_C.SOLVER.LR = CN(new_allowed=True)
_C.SOLVER.LR.METHOD = 'constant'
_C.SOLVER.LR.BASE = 0.1
