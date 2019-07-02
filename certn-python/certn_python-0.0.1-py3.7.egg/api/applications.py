from certn.api.api import API


class Applications(API):
    def invite(self, body):
        '''Send an email invitation to start an application'''

        return self.client.post('/api/v2/applications/invite/', data=body)

    def quick(self, body):
        '''Quick Application submission returns an unfinished application'''
        return self.client.post('/api/v2/applications/quick/', data=body)
