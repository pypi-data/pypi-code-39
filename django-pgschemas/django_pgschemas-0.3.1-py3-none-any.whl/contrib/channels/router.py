from django.conf import settings
from django.core.exceptions import ImproperlyConfigured
from django.utils.encoding import force_text
from django.utils.module_loading import import_string

from channels.routing import ProtocolTypeRouter, URLRouter

from ...schema import SchemaDescriptor
from ...utils import remove_www, get_tenant_model, get_domain_model
from .auth import TenantAuthMiddlewareStack


class TenantAwareProtocolTypeRouter(ProtocolTypeRouter):
    def __init__(self, application_mapping, tenant_prefix):
        self.tenant_prefix = tenant_prefix
        super().__init__(application_mapping)

    def __call__(self, scope):
        if scope["type"] != "http":
            scope["path"] = scope["path"][len(self.tenant_prefix) + 1 :]
        return super().__call__(scope)


class TenantProtocolRouter:
    """
    ProtocolRouter that handles multi-tenancy.
    """

    def __init__(self):
        self.root_ws_urlconf = settings.TENANTS["default"].get("WS_URLCONF")
        if self.root_ws_urlconf is None:
            raise ImproperlyConfigured(
                "TENANTS['default'] must contain a 'WS_URLCONF' key in order to use TenantProtocolRouter."
            )

    def get_tenant_scope(self, scope):
        """
        Get tenant and websockets urlconf based on scope host.
        """
        hostname = force_text(dict(scope["headers"]).get(b"host", b""))
        hostname = remove_www(hostname.split(":")[0])

        tenant = None
        ws_urlconf = self.root_ws_urlconf

        # Checking for static tenants
        for schema, data in settings.TENANTS.items():
            if schema in ["public", "default"]:
                continue
            if hostname in data["DOMAINS"]:
                tenant = SchemaDescriptor.create(schema_name=schema, domain_url=hostname)
                if "WS_URLCONF" in data:
                    ws_urlconf = data["WS_URLCONF"]
                return tenant, "", import_string(ws_urlconf + ".urlpatterns")

        # Checking for dynamic tenants
        else:
            DomainModel = get_domain_model()
            prefix = scope["path"].split("/")[1]
            try:
                domain = DomainModel.objects.select_related("tenant").get(domain=hostname, folder=prefix)
            except DomainModel.DoesNotExist:
                try:
                    domain = DomainModel.objects.select_related("tenant").get(domain=hostname, folder="")
                except DomainModel.DoesNotExist:
                    return None, "", []
            tenant = domain.tenant
            tenant.domain_url = hostname
            ws_urlconf = settings.TENANTS["default"]["WS_URLCONF"]
            return tenant, prefix if prefix == domain.folder else "", import_string(ws_urlconf + ".urlpatterns")

    def get_protocol_type_router(self, tenant_prefix, ws_urlconf):
        """
        Subclasses can override this to include more protocols.
        """
        return TenantAwareProtocolTypeRouter(
            {"websocket": TenantAuthMiddlewareStack(URLRouter(ws_urlconf))}, tenant_prefix
        )

    def __call__(self, scope):
        tenant, tenant_prefix, ws_urlconf = self.get_tenant_scope(scope)
        scope.update({"tenant": tenant})
        return self.get_protocol_type_router(tenant_prefix, ws_urlconf)(scope)
