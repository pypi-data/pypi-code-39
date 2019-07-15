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
"""Logger to control display"""
import os
import time
import logging
from datetime import datetime


class Logger():
  """Logger helper"""

  def __init__(self):
    self._start_timer = time.time()

  def init(self, name, output_dir, stdout=True):
    """Initilize the logger"""
    logging.root.handlers = []
    logging.basicConfig(format='%(message)s',
                        level=logging.DEBUG,
                        filename=os.path.join(output_dir, name + '.log'))
    self.logger = logging.getLogger(name)
    if stdout:
      ch = logging.StreamHandler()
      ch.setLevel(logging.DEBUG)
      ch.setFormatter(logging.Formatter('%(message)s'))
      self.logger.addHandler(ch)

  def _print(self, show_type, content):
    """Format print string"""
    str_date = '[' + \
        datetime.strftime(datetime.now(), '%y.%m.%d %H:%M:%S') + '] '
    self.logger.info(str_date + show_type + ' ' + content)

  def sys(self, content):
    self._print('[SYS]', content)

  def net(self, content):
    self._print('[NET]', content)

  def train(self, content):
    self._print('[TRN]', content)

  def val(self, content):
    self._print('[VAL]', content)

  def test(self, content):
    self._print('[TST]', content)

  def warn(self, content):
    self._print('[WAN]', content)

  def info(self, content):
    self._print('[INF]', content)

  def cfg(self, content):
    self._print('[CFG]', content)

  def error(self, content):
    self._print('[ERR]', content)

  def iters(self, cur_iter, keys, values):
    _data = 'Iter:%d' % cur_iter
    for i, key in enumerate(keys):
      if isinstance(values[i], int) or isinstance(values[i], str):
        _data += ', %s:%s' % (str(key), str(values[i]))
      elif key == 'lr':
        _data += ', %s:%.6f' % (str(key), float(values[i]))
      else:
        _data += ', %s:%.4f' % (str(key), float(values[i]))
    return _data

  def tic(self):
    self._start_timer = time.time()

  def toc(self):
    return (time.time() - self._start_timer) * 1000


logger = Logger()
