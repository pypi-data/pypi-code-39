from certn.api.api import API


class Applications(API):
    def invite(self, body):
        '''Send an email invitation to start an application'''

        return Application(self.client.post('/api/v2/applications/invite/', data=body))

    def quick(self, body):
        '''Quick Application submission returns an unfinished application'''
        return Application(self.client.post('/api/v2/applications/quick/', data=body))


class Application:
    def __init__(self, response):
        self.data = response

    @property
    def id(self):
        return self.data.get('id')

    @property
    def status(self):
        return self.data.get('status')

    def get(self, value, default=None):
        return self.data.get(value, default)
