from certn.api.api import API


class Applicants(API):
    def get(self, application_id):
        '''Get the application for a given application_id'''
        return self.client.get(f'/api/v2/applicants/{application_id}/')
