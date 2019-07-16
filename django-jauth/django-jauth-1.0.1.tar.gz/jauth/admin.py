from django.conf import settings
from django.contrib import admin
from .models import AccountKitUser, AccountKitAccessToken, FacebookAccessToken, FacebookUser, GoogleUser, \
    GoogleAccessToken


class JauthAdminBase(admin.ModelAdmin):
    pass


class AccountKitAdmin(JauthAdminBase):
    exclude = ()


class FacebookAdmin(JauthAdminBase):
    exclude = ()


class GoogleAdmin(JauthAdminBase):
    exclude = ()


admin.site.register(AccountKitUser, AccountKitAdmin)
admin.site.register(AccountKitAccessToken, AccountKitAdmin)
admin.site.register(FacebookUser, FacebookAdmin)
admin.site.register(FacebookAccessToken, FacebookAdmin)
admin.site.register(GoogleUser, GoogleAdmin)
admin.site.register(GoogleAccessToken, GoogleAdmin)

required_params = ['JAUTH_AUTHENTICATION_ERROR_REDIRECT', 'JAUTH_AUTHENTICATION_SUCCESS_REDIRECT']
for p in required_params:
    if not hasattr(settings, p):
        raise Exception('{} configuration missing'.format(p))
