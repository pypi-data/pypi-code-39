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
"""App.launch -> running multi-instance on a machine via multi-gpus
 NOTE: Current only support for single-machine with multi-gpus.
"""
import subprocess
import argparse

if __name__ == "__main__":
  parser = argparse.ArgumentParser(description="TensorWrapper Distributed \
    Launching is a high-level wrapper for torch.distributed, which could \
    specifiy the running device for each node.")
  parser.add_argument('--np', type=int, default=1,
                      help='The number of nodes to use for distributed')
  parser.add_argument('--dev', type=str, default=None,
                      help='Specify the device list e.g. cpu:0,cuda:1')
  parser.add_argument('script_args', nargs=argparse.REMAINDER,
                      help='Command: python3 main.py --config=...')
  args = parser.parse_args()

  # running processing
  cmd = ['horovodrun', '--verbose', '-np',
         str(args.np), '-H', 'localhost:%d' % args.np]
  cmd += args.script_args
  cmd += ['--dist=true', '--dist-device=' + args.dev]
  subprocess.run(cmd)
