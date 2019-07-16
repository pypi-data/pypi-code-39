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


__all__ = ["VsiOnNas", "VsiOnNasSchema"]
__pdoc__ = {
    "VsiOnNasSchema.resource": False,
    "VsiOnNas": False,
}


class VsiOnNasSchema(ResourceSchema):
    """The fields of the VsiOnNas object"""

    datastore = fields.Nested("VsiOnNasDatastoreSchema", unknown=EXCLUDE)
    r""" The datastore field of the vsi_on_nas.
 """
    hyper_v_access = fields.Nested("VdiOnNasHyperVAccessSchema", unknown=EXCLUDE)
    r""" The hyper_v_access field of the vsi_on_nas.
 """
    nfs_access = fields.Nested("AppNfsAccessSchema", unknown=EXCLUDE, many=True)
    r""" The list of NFS access controls. Optional in the POST body
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the vsi_on_nas.
 """

    @property
    def resource(self):
        return VsiOnNas

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "datastore",
            "hyper_v_access",
            "nfs_access",
            "protection_type",
        ]


class VsiOnNas(Resource):  # pylint: disable=missing-docstring

    _schema = VsiOnNasSchema
