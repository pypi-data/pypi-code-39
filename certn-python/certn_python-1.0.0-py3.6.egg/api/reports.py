from certn.api.api import API


class Reports(API):
    def pdf(self, application_id):
        return self.client.get(f'/api/v2/reports/{application_id}/pdf/')

    def link(self, application_id):
        return self.client.get(f'/api/v2/reports/{application_id}/link/')

    def web(self, application_id):
        return self.client.get(f'/api/v2/reports/{application_id}/web/')
