from certn.api.api import API


class Auth(API):

    path = '/api/v1'

    def login(self):
        '''basic authentication returns the user id and token'''
        response = self.client.post(
            path=f'{self.path}/authenticate/',
            data={'expires': None},
            is_authenticated=False,
        )

        return response.get('user_id'), response.get('token')

    def list(self):
        '''List all logged in sessions'''
        return self.client.get(path=f'{self.path}/authenticate/', is_authenticated=False)

    def logout(self):
        self.client.post(path=f'{self.path}/logout/', data=None, is_json=False)

    def logout_all(self):
        self.client.post(path=f'{self.path}/logoutall/', data=None, is_json=False)
