from flask import jsonify
import python_freeipa
from .config import config

ipa_host = config.IPA_HOST
ipa_user = config.PRINCIPAL
ipa_password = config.PASSWORD


def ipa_add_host(hostname, ip):
    '''
    This function adds a host in IPA and returns the hostname, ip, and OTP

    :param hostname: Hostname of host to add to IPA
    :type hostname: string
    :param ip: Private IP Address of host to add to IPA
    :type ip: unicode
    '''
    ipa_client = python_freeipa.Client(
            ipa_host,
            verify_ssl=False,
            version='2.215'
            )
    ipa_client.login(ipa_user,
                     ipa_password
                     )
    host = ipa_client.host_add(
            hostname,
            random=True,
            ip_address=ip
        )
    response = jsonify(
            {'hostname': hostname,
             'password': host.get('randompassword'),
             'ip': ip
             }
            )
    response.status_code = 201
    return response


def ipa_delete_host(hostname, ip):
    '''
    This function removes a host in IPA

    :param hostname: Hostname of host to add to IPA
    :type hostname: string
    '''
    ipa_client = python_freeipa.Client(
            ipa_host,
            verify_ssl=False,
            version='2.215'
            )
    ipa_client.login(ipa_user,
                     ipa_password
                     )
    ipa_client.host_del(hostname, updatedns=True)


def ipa_verify_host(hostname):
    '''
    This function checks to see if a host entry exists for the provided
    hostname

    :param hostname: Hostname of host to lookup in IPA
    :type hostname: string
    '''

    ipa_client = python_freeipa.Client(
            ipa_host,
            verify_ssl=False,
            version='2.215'
            )
    ipa_client.login(ipa_user,
                     ipa_password
                     )
    print(hostname)
    if ipa_client.host_find(criteria=hostname, fqdn=hostname):
        return True
    else:
        return False
