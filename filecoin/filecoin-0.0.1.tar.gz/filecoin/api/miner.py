# coding: utf8
import os
from filecoin.utils import run_filecoin_cmd, run_command

from .node import get_node_info



def create_miner(blocks=100, wallet=None):
    # 1 block = 256 Mb
    # maybe will wait minutes
    node_info = get_node_info()
    node_id = node_info['ID']
    pledge = round(blocks * 0.001, 3)
    cmd = 'miner create %s %s --gas-price=0.000000001 --gas-limit=1000 --peerid=%s' % (blocks, pledge, node_id,)
    if wallet:
        cmd += ' --from=%s' % wallet
    print('go-filecoin %s' % cmd)
    result = run_filecoin_cmd(cmd)
    miner_address = result.strip()
    return miner_address


def start_to_mind():
    run_filecoin_cmd('mining start')




def get_miner_info(miner):
    owner = run_filecoin_cmd('miner owner %s' % miner)
    pledge = run_filecoin_cmd('miner pledge %s' % miner)
    pledge = float(pledge)
    power = run_filecoin_cmd('miner power %s' % miner)
    info = dict(
        miner = miner,
        owner = owner,
        power = power,
        pledge = pledge,
    )
    return info



def create_file_and_get_cid():
    tmp_filepath = '/tmp/filecoin_file.data'
    cmd = 'dd if=/dev/urandom of=%s bs=20M count=10' % tmp_filepath
    run_command(cmd)
    filecoin_cmd = 'client import %s' % tmp_filepath
    cid = run_filecoin_cmd(filecoin_cmd)
    os.remove(tmp_filepath)
    return cid


