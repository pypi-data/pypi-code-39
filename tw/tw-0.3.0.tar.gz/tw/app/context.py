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
"""App.Context
  It will offer a set of standard context to manage network running.

INFO:
  NAME:
  DIR:
  DEVICE:
  TASK:
  OUTPUTS:

MODEL:
  WEIGHT:
"""

from datetime import datetime
import torch
import torch.utils.tensorboard as tb

from tw.utils.logger import logger
from tw.utils import filesystem as fs
from tw.solver.checkpoint import Snapshot


class ContextBase():
  def __init__(self, config, **args):
    # Initialize ENV
    if args['device'] is not None:
      config.INFO.DEVICE = args['device']
    if args['task'] is not None:
      config.INFO.TASK = args['task']
    if args['model'] is not None:
      config.MODEL.WEIGHT = args['model']
    if args['dir']:
      config.INFO.DIR = args['dir']

    # create pid for folder
    pid = datetime.strftime(datetime.now(), '%y%m%d%H%M%S')
    if config.DIST.RUN:
      pid += '.%s.p%d' % (config.DIST.HOSTNAME, config.DIST.RANK)

    # create folder
    if config.INFO.DIR is None:
      config.INFO.DIR = "%s/%s.%s" % (config.INFO.OUTPUTS,
                                      config.INFO.NAME, pid)
      fs.mkdirs(config.INFO.DIR, raise_path_exits=True)
    else:
      fs.mkdirs(config.INFO.DIR)

    # initialize logger
    logger.init(name=config.INFO.NAME + '-' + pid,
                output_dir=config.INFO.DIR,
                stdout=config.DIST.IS_ROOT)
    logger.info('Initilized logger successful.')
    logger.info('Current cmd %s' % str(args))
    logger.info('Current model in %s' % config.INFO.DIR)
    logger.info('Cuurent device in %s' % config.INFO.DEVICE)
    logger.info('\n'+str(config))

    # initialize config
    self.C = config
    self.A = args

    # global state
    self.GlobalStep = 0
    self.GlobalEpoch = 0

    # Statistic
    self.Device = torch.device(self.C.INFO.DEVICE)
    self.Writer = tb.SummaryWriter(log_dir=self.C.INFO.DIR)
    self.Snapshot = Snapshot(self.C.INFO.NAME, self.C.INFO.DIR, self.Writer)

  def GetSavePath(self, count: int):
    return '%s/%s.%d.ptr.tar' % (self.C.INFO.DIR, self.C.INFO.NAME, count)

  def ReachInterval(self, step, interval: int):
    if interval and \
       interval > 0 and \
       step % interval == 0:
      return True
    return False

  def ReachGlobalInterval(self, interval):
    return self.ReachInterval(self.GlobalStep, interval)

  def train(self, *args, **kwargs):
    raise NotImplementedError(self.train.__name__)

  def val(self, *args, **kwargs):
    raise NotImplementedError(self.val.__name__)

  def test(self, *args, **kwargs):
    raise NotImplementedError(self.test.__name__)

  def inference(self, *args, **kwargs):
    raise NotImplementedError(self.inference.__name__)
