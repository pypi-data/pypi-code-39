from .base import BaseAnsibleTowerModule


class LookupModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'kind': {'type': 'str', 'required': True},
        'params': {'type': 'dict', 'required': False},
    }
    object_types = {
        'Credential': 'credentials',
        'CredentialType': 'credential_types',
    }

    def facts_only(self):
        return True

    def getsubjectresource(self):
        kind = self.params['kind']
        return self.client.list(self.object_types[kind],
            params=self.params['params'])
