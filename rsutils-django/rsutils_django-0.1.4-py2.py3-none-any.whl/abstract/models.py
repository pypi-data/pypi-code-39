from uuid import uuid4
from safedelete.models import SafeDeleteModel
from django.contrib.auth.models import AbstractUser
from django.db.models import DateTimeField, UUIDField, CharField, FloatField


class RSModel(SafeDeleteModel):
    updated_at = DateTimeField(auto_now=True)
    created_at = DateTimeField(auto_now_add=True)
    id = UUIDField(primary_key=True, default=uuid4, editable=False)

    class Meta:
        abstract = True


class RSUser(AbstractUser, RSModel):

    REQUIRED_FIELDS = ['email', 'username']

    class Meta:
        abstract = True


class RSAddress(RSModel):
    city = CharField(max_length=50)
    state = CharField(max_length=50)
    street = CharField(max_length=100)
    country = CharField(max_length=100)
    district = CharField(max_length=100)
    address_1 = CharField(max_length=250)
    address_2 = CharField(max_length=250, null=True, blank=True)
    latitude = FloatField(max_length=100, null=True, blank=True)
    longitude = FloatField(max_length=100, null=True, blank=True)
    postal_code = CharField(max_length=10, null=True, blank=True)

    class Meta:
        abstract = True
