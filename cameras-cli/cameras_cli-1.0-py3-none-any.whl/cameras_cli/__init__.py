import argparse

import netifaces as netifaces
import requests


def parse_args():
    parser = argparse.ArgumentParser(
        description="Cameras CLI"
    )
    parser.add_argument(
        '--command',
        type=str,
        required=True,
        help='Command to execute'
    )
    parser.add_argument(
        '--options',
        type=str,
        required=False,
        help='Options to this command'
    )

    return parser.parse_args()


def get_wlan_ip(network_interface):
    result = netifaces.ifaddresses(network_interface)

    return [
        config for config in [
            config[0] for key, config in result.items()
        ] if 'addr' in config and 'netmask' in config
    ][0]


def register_realm(opts):
    core_api_host, network_interface = opts.split(' ')
    wlan_ip = get_wlan_ip(network_interface)

    requests.post(core_api_host, data="""
        mutation {
          createRealm (newRealm: {name: "{}", ip: "{}"}) {
            ok
            realm {
              id
              key
            }
          }
        }
    """.format(wlan_ip['addr'], wlan_ip['addr']))


def validate_params_register_realm(opts):
    return opts is not None


def cameras(params):
    commands = {
        'register_realm':  {
            'fn': register_realm,
            'validator': validate_params_register_realm
        }
    }
    cmd = params.command

    validator_fn = commands[cmd]['validator']

    if validator_fn(params.options):
        cmd_fn = commands[cmd]['fn']
        cmd_fn(params.options)


def main():
    cameras(parse_args())