import gnupg
from pprint import pprint
unencrypted_string = '{"valid_until": "2019-03-19T09:07:10.096722Z", "cn": "Jonathan SCHAEFFER", "memberof": "/epos;/", "sn": "SCHAEFFER", "issued": "2019-03-18T09:07:10.096727Z", "mail": "jonathan.schaeffer@univ-grenoble-alpes.fr", "givenName": "Jonathan", "expiration": "1d"}'
recipient = '4169CE9D00970757'
gpg = gnupg.GPG(gnupghome='./test_files/gpg_home')
key_data = open('test_files/test-eidaauth-private.asc').read()

import_result = gpg.import_keys(key_data)
pprint(import_result.results)
pprint(gpg.list_keys())


encrypted_data = gpg.encrypt(unencrypted_string, 'nonone@tests.org', always_trust=True)
encrypted_string = str(encrypted_data)
print('ok: ', encrypted_data.ok)
print('status: ', encrypted_data.status)
print('stderr: ', encrypted_data.stderr)
print('unencrypted_string: ', unencrypted_string)
print('encrypted_string: ', encrypted_string)
