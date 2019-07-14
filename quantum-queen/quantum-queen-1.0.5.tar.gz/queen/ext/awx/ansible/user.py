from .base import BaseAnsibleTowerModule


class UserModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'facts': {'type': 'bool', 'required': False, 'default': False},
        'username': {'type': 'str', 'required': True},
        'password': {'type': 'str', 'required': False, 'no_log': True},
    }

    def getsubjectresource(self):
        return self.client.list('users',
            params={'username': self.params['username']})

    def dtofromparams(self):
        dto = {
            'username': self.params['username'],
        }
        if not self.resource:
            if not self.params.get('password'):
                self.fail("`password` is required when creating new users.")
                return
            dto['password'] = self.params['password']
        return dto

    def getcreateurlparts(self):
        return ['POST', 'users']

    def getupdateurlparts(self):
        return ['PUT', 'users', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'users', self.resource['id']]

