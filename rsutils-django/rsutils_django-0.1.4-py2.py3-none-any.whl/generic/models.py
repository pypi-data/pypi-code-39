from django.db.models import UUIDField, ForeignKey, CASCADE
from django.contrib.contenttypes.models import ContentType
from django.contrib.contenttypes.fields import GenericForeignKey

from rsutils_django.abstract.models import RSAddress


class RSGenericAddress(RSAddress):
    object_id = UUIDField()
    content_type = ForeignKey(ContentType, on_delete=CASCADE)
    content_object = GenericForeignKey('content_type', 'object_id')

    class Meta:
        abstract = True
