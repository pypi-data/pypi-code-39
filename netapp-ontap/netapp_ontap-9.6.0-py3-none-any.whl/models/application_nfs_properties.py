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


__all__ = ["ApplicationNfsProperties", "ApplicationNfsPropertiesSchema"]
__pdoc__ = {
    "ApplicationNfsPropertiesSchema.resource": False,
    "ApplicationNfsProperties": False,
}


class ApplicationNfsPropertiesSchema(ResourceSchema):
    """The fields of the ApplicationNfsProperties object"""

    backing_storage = fields.Nested("ApplicationCifsPropertiesBackingStorageSchema", unknown=EXCLUDE)
    r""" The backing_storage field of the application_nfs_properties.
 """
    export_policy = fields.Nested("ApplicationNfsPropertiesExportPolicySchema", unknown=EXCLUDE)
    r""" The export_policy field of the application_nfs_properties.
 """
    ips = fields.List(fields.Str)
    r""" The ips field of the application_nfs_properties.
 """
    path = fields.Str()
    r""" Junction path
 """
    permissions = fields.Nested("ApplicationNfsPropertiesPermissionsSchema", unknown=EXCLUDE, many=True)
    r""" The permissions field of the application_nfs_properties.
 """

    @property
    def resource(self):
        return ApplicationNfsProperties

    @property
    def patchable_fields(self):
        return [
            "ips",
        ]

    @property
    def postable_fields(self):
        return [
            "backing_storage",
            "export_policy",
            "ips",
        ]


class ApplicationNfsProperties(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationNfsPropertiesSchema
