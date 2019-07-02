from certn.api.api import API


class Reports(API):
    path = '/api/v2/reports'

    def pdf(self, application_id):
        return self.client.get(f'{self.path}/{application_id}/pdf/', is_json=False)

    def link(self, application_id):
        return self.client.get(f'{self.path}/{application_id}/link/')

    def web(self, application_id):
        return self.client.get(f'{self.path}/{application_id}/web/', is_json=False)
