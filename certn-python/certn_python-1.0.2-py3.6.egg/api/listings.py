from certn.api.api import API


class Listings(API):
    def list(self):
        return self.client.get('/api/v2/listings/')

    def get(self, listing_id):
        return self.client.get(f'/api/v2/listings/{listing_id}/')

    def add(self, data):
        return self.client.post('/api/v2/listings/', data)

    def update(self, listing_id, data):
        return self.client.put(f'/api/v2/listings/{listing_id}/', data)

    def delete(self, listing_id):
        return self.client.delete(f'/api/v2/listings/{listing_id}/')
