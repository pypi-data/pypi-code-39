from .base import BaseAnsibleTowerModule


class CredentialModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'credential_type': {'required': False},
        'organization_id': {'type': 'int', 'required': True},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False},
        'inputs': {'type': 'dict', 'required': False},
    }

    def getsubjectresource(self):
        params={
            'name': self.params['name'],
            'organization_id': self.params['organization_id']
        }
        if self.params.get('credential_type'):
            params['credential_type'] = self.params['credential_type']
        return self.client.list('credentials', params=params)

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

    def run(self):
        if not self.facts_only() and not self.params.get('inputs'):
            self.fail("The `inputs` parameter is required.")
        if not self.facts_only() and not self.params.get('credential_type'):
            self.fail("The `credential_type` parameter is required.")
        if not self.facts_only() and not self.params.get('description'):
            self.fail("The `description` parameter is required.")
        return super().run()

