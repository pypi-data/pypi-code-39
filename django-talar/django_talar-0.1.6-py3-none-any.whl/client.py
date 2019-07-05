import json

from django.conf import settings

from .crypto import AESCipherBase64
from .serializers import PaymentSerializer


class Talar:
    """
    Talar integration class. Used to perform actions for Talar API.
    """

    def __init__(self):
        self.project_id = settings.TALAR['project_id']

        self.access_key_id = settings.TALAR['access_key_id']
        self.access_key = settings.TALAR['access_key']

        self.url = f'https://talar.app/{self.project_id}/order/classic/create/'

    def create_payment_data(self, data: dict):
        talar_serializer = PaymentSerializer(data=data)
        talar_serializer.is_valid(raise_exception=True)
        encrypted_data = AESCipherBase64(key=self.access_key).encrypt(
            data=json.dumps(talar_serializer.validated_data)
        )
        return encrypted_data
