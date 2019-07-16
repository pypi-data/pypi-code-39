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


__all__ = ["VsiOnSan", "VsiOnSanSchema"]
__pdoc__ = {
    "VsiOnSanSchema.resource": False,
    "VsiOnSan": False,
}


class VsiOnSanSchema(ResourceSchema):
    """The fields of the VsiOnSan object"""

    datastore = fields.Nested("VsiOnNasDatastoreSchema", unknown=EXCLUDE)
    r""" The datastore field of the vsi_on_san.
 """
    hypervisor = fields.Str()
    r""" The name of the hypervisor hosting the application. Required in the POST body

Valid choices:

* hyper_v
* vmware
* xen """
    igroup_name = fields.Str()
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. Required in the POST body and optional in the PATCH body
 """
    new_igroups = fields.Nested("VsiOnSanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the vsi_on_san.
 """

    @property
    def resource(self):
        return VsiOnSan

    @property
    def patchable_fields(self):
        return [
            "igroup_name",
        ]

    @property
    def postable_fields(self):
        return [
            "datastore",
            "hypervisor",
            "igroup_name",
            "new_igroups",
            "protection_type",
        ]


class VsiOnSan(Resource):  # pylint: disable=missing-docstring

    _schema = VsiOnSanSchema
