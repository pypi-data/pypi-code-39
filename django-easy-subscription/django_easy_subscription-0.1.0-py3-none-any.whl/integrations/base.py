from django.core.exceptions import ImproperlyConfigured


class BaseIntegration:
    required_credentials = []

    def __init__(self, **credentials):
        for key, value in credentials.items():
            setattr(self, key, value)

        for credential in self.required_credentials:
            if not hasattr(self, credential):
                raise ImproperlyConfigured(
                    '`{}` must be set to use {} integration'.format(credential, self.__class__.__name__)
                )

    def subscribe(self, subscriber):
        raise NotImplementedError

    def unsubscribe(self, subscriber, delete=False):
        raise NotImplementedError
