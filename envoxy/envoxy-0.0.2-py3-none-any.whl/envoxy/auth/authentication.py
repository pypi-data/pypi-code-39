from ..views import View
from flask import request



class AuthRequiredView(View):

    valid_token = 'admin'


    def has_valid_token(self):

        auth_header = request.headers.get('Authorization', '').split()
        access_token = auth_header[0] if len(auth_header) == 1 else auth_header[1:]

        return access_token == self.valid_token
    
    
    def _dispatch(self, _method, _protocol):
        super(AuthRequiredView, self)._dispatch(_method, _protocol)

        if not self.has_valid_token():
            raise Exception('Invalid Token')





