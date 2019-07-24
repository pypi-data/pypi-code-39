from django.conf import settings
from django.contrib.auth import get_user_model

class EmailOrUsernameModelBackend(object):
    def authenticate(self, request, username=None, password=None):
        user = get_user_model()
        if '@' in username:
            kwargs = {'email': username}
        else:
            kwargs = {'username': username}
        try:
            user = user.objects.get(**kwargs)
            if user.check_password(password):
                return user
        except user.DoesNotExist:
            return None
    
    def get_user(self, user_id):
        user = get_user_model()
        try:
            return user.objects.get(pk=user_id)
        except user.DoesNotExist:
            return None