from .base import BaseAnsibleTowerModule


class CredentialTypeModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False},
        'kind': {'type': 'str', 'required': False, 'default': 'cloud'},
        'inputs': {'type': 'dict', 'required': False},
        'injectors': {'type': 'dict', 'required': False},
    }

    def getsubjectresource(self):
        return self.client.list(
            'credential_types',
            params={
                'name': self.params['name'],
                'kind': self.params['kind']
            })

    def dtofromparams(self):
        return {
            'name': self.params['name'],
            'description': str.strip(self.params['description']),
            'kind': self.params['kind'],
            'inputs': self.params['inputs'],
            'injectors': self.params['injectors']
        }

    def getcreateurlparts(self):
        return ['POST', 'credential_types']

    def getupdateurlparts(self):
        return ['PUT', 'credential_types', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'credential_types', self.resource['id']]

