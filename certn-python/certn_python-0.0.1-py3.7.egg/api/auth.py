from certn.api.api import API


class Auth(API):
    def login(self):
        '''basic authentication returns the user id and token'''
        response = self.client.post(
            path='/api/v1/authenticate/', data={'expires': None}, is_authenticated=False
        )

        return response.get('user_id'), response.get('token')

    def list(self):
        '''List all logged in sessions'''
        return self.client.get(path='/api/v1/authenticate/', is_authenticated=False)

    def logout(self):
        self.client.post(path='/api/v1/logout/', data=None, is_json=False)

    def logout_all(self):
        self.client.post(path='/api/v1/logoutall/', data=None, is_json=False)
