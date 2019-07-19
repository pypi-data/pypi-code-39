import netifaces as netifaces

import click
import requests


def get_wlan_ip(network_interface):
    result = netifaces.ifaddresses(network_interface)

    return [
        config for config in [
            config[0] for key, config in result.items()
        ] if 'addr' in config and 'netmask' in config
    ][0]


@click.command()
@click.argument('core_api_host')
@click.argument('network_interface')
def register_realm(core_api_host, network_interface):
    wlan_ip = get_wlan_ip(network_interface)['addr']

    url = "{}/graphql/".format(core_api_host)

    mutation = """
        mutation {
          createRealm (newRealm: {name: "%s", ip: "%s"}) {
            ok
            realm {
              id
              key
            }
          }
        }
    """ % (wlan_ip, wlan_ip)

    response = requests.post(url, data=mutation, headers={
        'Content-Type': 'application/graphql'
    })

    click.echo(response.json())


@click.group()
def cameras():
    pass


cameras.add_command(register_realm)
