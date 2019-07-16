# pylint: disable=trailing-newlines
# pylint: disable=line-too-long
# pylint: disable=too-many-lines
# pylint: disable=unused-import
# pylint: disable=invalid-name

r"""
Copyright &copy; 2019 NetApp Inc.
All rights reserved.


"""

from marshmallow import EXCLUDE, fields  # type: ignore
from netapp_ontap.resource import Resource, ResourceSchema


__all__ = ["ApplicationBackingStorage", "ApplicationBackingStorageSchema"]
__pdoc__ = {
    "ApplicationBackingStorageSchema.resource": False,
    "ApplicationBackingStorage": False,
}


class ApplicationBackingStorageSchema(ResourceSchema):
    """The fields of the ApplicationBackingStorage object"""

    luns = fields.Nested("ApplicationLunObjectSchema", unknown=EXCLUDE, many=True)
    r""" The luns field of the application_backing_storage.
 """
    volumes = fields.Nested("ApplicationVolumeObjectSchema", unknown=EXCLUDE, many=True)
    r""" The volumes field of the application_backing_storage.
 """

    @property
    def resource(self):
        return ApplicationBackingStorage

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "luns",
            "volumes",
        ]


class ApplicationBackingStorage(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationBackingStorageSchema
