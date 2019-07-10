from .base import BaseAnsibleTowerModule


class TeamModule(BaseAnsibleTowerModule):
    module_args = {
        'api_url': {'type': 'str', 'required': False},
        'api_user': {'type': 'str', 'required': False},
        'api_password': {'type': 'str', 'required': False, 'no_log': True},
        'validate_certs': {'type': 'bool', 'required': False, 'default': False},
        'state': {'type': 'str', 'required': False, 'default': 'present'},
        'organization_id': {'type': 'int', 'required': True},
        'name': {'type': 'str', 'required': True},
        'description': {'type': 'str', 'required': False, 'default': ''},
    }

    @property
    def organization_id(self):
        return self.params['organization_id']

    def getsubjectresource(self):
        return self.client.list(
            'teams',
            params={
                'name': self.params['name'],
                'organization': self.organization_id
            })

    def dtofromparams(self):
        return {
            'name': self.params['name'],
            'description': self.params['description'],
            'organization': self.organization_id
        }

    def getcreateurlparts(self):
        return ['POST', 'teams']

    def getupdateurlparts(self):
        return ['PUT', 'teams', self.resource['id']]

    def getdeleteurlparts(self):
        return ['DELETE', 'teams', self.resource['id']]
