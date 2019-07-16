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


__all__ = ["Nas", "NasSchema"]
__pdoc__ = {
    "NasSchema.resource": False,
    "Nas": False,
}


class NasSchema(ResourceSchema):
    """The fields of the Nas object"""

    application_components = fields.Nested("NasApplicationComponentsSchema", unknown=EXCLUDE, many=True)
    r""" The application_components field of the nas.
 """
    cifs_access = fields.Nested("AppCifsAccessSchema", unknown=EXCLUDE, many=True)
    r""" The list of CIFS access controls. Optional in the POST body
 """
    nfs_access = fields.Nested("AppNfsAccessSchema", unknown=EXCLUDE, many=True)
    r""" The list of NFS access controls. Optional in the POST body
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the nas.
 """

    @property
    def resource(self):
        return Nas

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "application_components",
            "cifs_access",
            "nfs_access",
            "protection_type",
        ]


class Nas(Resource):  # pylint: disable=missing-docstring

    _schema = NasSchema
