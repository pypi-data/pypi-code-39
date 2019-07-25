from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig as BaseConfig

class AdminpanelConfig(BaseConfig):
	name = 'adminpanel'
	verbose_name = _('Admin Panel')
