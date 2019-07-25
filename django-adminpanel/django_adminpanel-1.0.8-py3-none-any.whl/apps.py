from django.utils.translation import ugettext_lazy as _
from django.apps import AppConfig as BaseConfig

class ApblogsConfig(BaseConfig):
	name = 'apblogs'
	verbose_name = _('Admin Panel Blog')
