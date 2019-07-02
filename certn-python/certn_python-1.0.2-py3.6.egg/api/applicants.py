from certn.api.api import API
from certn.api.applications import Application


class Applicants(API):
    def get(self, application_id):
        '''Get the application for a given application_id'''
        return Application(self.client.get(f'/api/v2/applicants/{application_id}/'))
