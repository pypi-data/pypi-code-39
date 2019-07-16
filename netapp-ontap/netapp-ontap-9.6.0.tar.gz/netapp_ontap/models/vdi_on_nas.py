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


__all__ = ["VdiOnNas", "VdiOnNasSchema"]
__pdoc__ = {
    "VdiOnNasSchema.resource": False,
    "VdiOnNas": False,
}


class VdiOnNasSchema(ResourceSchema):
    """The fields of the VdiOnNas object"""

    desktops = fields.Nested("VdiOnNasDesktopsSchema", unknown=EXCLUDE)
    r""" The desktops field of the vdi_on_nas.
 """
    hyper_v_access = fields.Nested("VdiOnNasHyperVAccessSchema", unknown=EXCLUDE)
    r""" The hyper_v_access field of the vdi_on_nas.
 """
    nfs_access = fields.Nested("AppNfsAccessSchema", unknown=EXCLUDE, many=True)
    r""" The list of NFS access controls. Optional in the POST body
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the vdi_on_nas.
 """

    @property
    def resource(self):
        return VdiOnNas

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "desktops",
            "hyper_v_access",
            "nfs_access",
            "protection_type",
        ]


class VdiOnNas(Resource):  # pylint: disable=missing-docstring

    _schema = VdiOnNasSchema
