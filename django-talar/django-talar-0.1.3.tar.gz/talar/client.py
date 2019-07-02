import json

from django.conf import settings

from .crypto import AESCipherBase64
from .serializers import TalarSerializer


class Talar:
    """
    Talar integration class. Used to perform actions for Talar API.
    """

    def __init__(self):
        self.key_id = settings.TALAR['secret_key']
        self.token = settings.TALAR['token']
        self.project_id = settings.TALAR['project_id']
        self.url = 'https://talar.app/{}/order/classic/create/'.format(
            self.project_id
        )

    def create_payment_data(self, data: dict):
        talar_serializer = TalarSerializer(data=data)
        talar_serializer.is_valid(raise_exception=True)
        encrypted_data = AESCipherBase64(key=self.key_id).encrypt(
            data=json.dumps(talar_serializer.validated_data)
        )
        return encrypted_data
