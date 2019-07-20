# -*- coding: utf-8 -*-
# Design by zhaoguanzhi
# Email: zhaoguanzhi1992@163.com

import os
from helper import get_args
from runs.ner_sample_maker import prepare

args = get_args()
if True:
    import sys
    param_str = '\n'.join(['%20s = %s' % (k, v) for k, v in sorted(vars(args).items())])
    print('usage: %s\n%20s   %s\n%s\n%s\n' % (' '.join(sys.argv), 'ARG', 'VALUE', '_' * 50, param_str))

os.environ['CUDA_VISIBLE_DEVICES'] = args.device_map
prepare(args=args)