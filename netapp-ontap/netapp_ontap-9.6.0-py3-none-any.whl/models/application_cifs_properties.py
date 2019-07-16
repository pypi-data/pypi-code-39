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


__all__ = ["ApplicationCifsProperties", "ApplicationCifsPropertiesSchema"]
__pdoc__ = {
    "ApplicationCifsPropertiesSchema.resource": False,
    "ApplicationCifsProperties": False,
}


class ApplicationCifsPropertiesSchema(ResourceSchema):
    """The fields of the ApplicationCifsProperties object"""

    backing_storage = fields.Nested("ApplicationCifsPropertiesBackingStorageSchema", unknown=EXCLUDE)
    r""" The backing_storage field of the application_cifs_properties.
 """
    ips = fields.List(fields.Str)
    r""" The ips field of the application_cifs_properties.
 """
    path = fields.Str()
    r""" Junction path
 """
    permissions = fields.Nested("ApplicationCifsPropertiesPermissionsSchema", unknown=EXCLUDE, many=True)
    r""" The permissions field of the application_cifs_properties.
 """
    server = fields.Nested("ApplicationCifsPropertiesServerSchema", unknown=EXCLUDE)
    r""" The server field of the application_cifs_properties.
 """
    share = fields.Nested("ApplicationCifsPropertiesShareSchema", unknown=EXCLUDE)
    r""" The share field of the application_cifs_properties.
 """

    @property
    def resource(self):
        return ApplicationCifsProperties

    @property
    def patchable_fields(self):
        return [
            "ips",
        ]

    @property
    def postable_fields(self):
        return [
            "backing_storage",
            "ips",
            "server",
            "share",
        ]


class ApplicationCifsProperties(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationCifsPropertiesSchema
