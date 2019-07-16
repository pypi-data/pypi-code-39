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


__all__ = ["ApplicationSanAccess", "ApplicationSanAccessSchema"]
__pdoc__ = {
    "ApplicationSanAccessSchema.resource": False,
    "ApplicationSanAccess": False,
}


class ApplicationSanAccessSchema(ResourceSchema):
    """The fields of the ApplicationSanAccess object"""

    backing_storage = fields.Nested("ApplicationCifsPropertiesBackingStorageSchema", unknown=EXCLUDE)
    r""" The backing_storage field of the application_san_access.
 """
    is_clone = fields.Boolean()
    r""" Clone
 """
    lun_mappings = fields.Nested("ApplicationLunMappingObjectSchema", unknown=EXCLUDE, many=True)
    r""" The lun_mappings field of the application_san_access.
 """
    serial_number = fields.Str()
    r""" LUN serial number
 """

    @property
    def resource(self):
        return ApplicationSanAccess

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "backing_storage",
            "lun_mappings",
        ]


class ApplicationSanAccess(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationSanAccessSchema
