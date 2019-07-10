from rsutils_django.abstract.models import RSModel

try:
    from tenant_schemas.models import TenantMixin
except ImportError:
    raise ImportError('pipenv install django-tenant-schemas')


class RSTenantMixin(RSModel, TenantMixin):

    class Meta:
        abstract = True
