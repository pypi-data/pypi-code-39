from .base import BaseAnsibleTowerModule


class CredentialModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'credential_type': {'type': 'int', 'required': True},
        'organization_id': {'type': 'int', 'required': True},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': True},
        'inputs': {'type': 'dict', 'required': True},
    }

    def getsubjectresource(self):
        return self.client.list(
            'credentials',
            params={
                'name': self.params['name'],
                'credential_type': self.params['credential_type']
            })

    def dtofromparams(self):
        return {
            'credential_type': self.params['credential_type'],
            'organization': self.params['organization_id'],
            'name': self.params['name'],
            'description': str.strip(self.params['description']),
            'inputs': self.params['inputs'],
        }

    def getcreateurlparts(self):
        return ['POST', 'credentials']

    def getupdateurlparts(self):
        return ['PUT', 'credentials', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'credentials', self.resource['id']]

