from django.apps import AppConfig
from django.utils.translation import ugettext_lazy as _


class JauthConfig(AppConfig):
    name = 'jauth'
    verbose_name = _('OAuth2 Authentication')
