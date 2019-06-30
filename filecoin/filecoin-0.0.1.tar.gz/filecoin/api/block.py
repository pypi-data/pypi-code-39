# coding: utf8
from filecoin.utils import run_filecoin_cmd
import re


def get_current_height():
    chain_head = run_filecoin_cmd('chain head')
    result = run_filecoin_cmd('show block %s' % chain_head)
    try:
        height = re.search('Height: *(\d+)', result).group(1)
        height = int(height.strip())
    except:
        height = None
    return height


