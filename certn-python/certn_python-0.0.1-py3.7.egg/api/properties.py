from certn.api.api import API


class Properties(API):
    def list(self):
        return self.client.get('/api/v2/properties/')

    def get(self, property_id):
        return self.client.get(f'/api/v2/properties/{property_id}')

    def add(self, data):
        return self.client.post('/api/v2/properties/', data)

    def update(self, property_id, data):
        return self.client.put(f'/api/v2/properties/{property_id}/', data)

    def delete(self, property_id):
        return self.client.delete(f'/api/v2/properties/{property_id}/')
