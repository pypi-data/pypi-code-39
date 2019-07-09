#!/usr/bin/env python3
import socket

from ansible.module_utils.basic import AnsibleModule


module = AnsibleModule(
    argument_spec=dict(
        ip=dict(type='str', required=True)
    ),
    supports_check_mode=True
)

ip = module.params['ip']
s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
c = False

for port in (22, 2222):
    try:
        c = s.connect((ip, port))
    except:
        continue
    else:
        s.close()
        break

if c is False:
    return module.fail_json(msg='Could not connect to ' + ip)

module.exit_json(changed=False, message=port)
