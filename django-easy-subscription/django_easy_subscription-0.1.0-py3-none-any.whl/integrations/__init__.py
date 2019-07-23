import importlib
from django.core.exceptions import ImproperlyConfigured
from ..conf import settings


def get_integration():
    if settings.EASY_SUBSCRIPTION_INTEGRATION is None:
        raise ImproperlyConfigured('No integration selected, please set NEWSLETTER_FORM_INTEGRATION')

    if not settings.EASY_SUBSCRIPTION_INTEGRATION_CREDENTIALS:
        raise ImproperlyConfigured(
            'Integration credentials missing, please set NEWSLETTER_FORM_INTEGRATION_CREDENTIALS'
        )

    try:
        integration_module = importlib.import_module(settings.EASY_SUBSCRIPTION_INTEGRATION)
        integration = integration_module.integration_class(**settings.EASY_SUBSCRIPTION_INTEGRATION_CREDENTIALS)
        return integration
    except ModuleNotFoundError:
        raise ImproperlyConfigured('The selected integration is not valid')
