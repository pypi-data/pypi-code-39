# coding: utf8
from filecoin.utils import run_filecoin_cmd, run_command
import json
import re
import os

def get_node_info():
    result = run_filecoin_cmd('id')
    info = json.loads(result)
    return info





def re_config_node(docker_container_name):
    raw_result = run_command('docker inspect %s' % docker_container_name)
    result = json.loads(raw_result)
    info = result[0]
    port = int(info['Config']['ExposedPorts'].keys()[0].replace('/tcp', ''))
    data_dir = info['Mounts'][0]['Source']
    config_filepath = os.path.join(data_dir, 'config.json')
    with open(config_filepath, 'rb') as f:
        configs = json.loads(f.read())
    node_address = '/ip4/0.0.0.0/tcp/%s' % port
    configs['swarm']['address'] = node_address
    configs['observability']['metrics']['prometheusEndpoint'] = node_address
    with open(config_filepath, 'wb') as f:
        f.write(json.dumps(configs, indent=4))
    run_command('docker restart %s' % docker_container_name)


