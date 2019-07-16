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


__all__ = ["VdiOnSanNewIgroups", "VdiOnSanNewIgroupsSchema"]
__pdoc__ = {
    "VdiOnSanNewIgroupsSchema.resource": False,
    "VdiOnSanNewIgroups": False,
}


class VdiOnSanNewIgroupsSchema(ResourceSchema):
    """The fields of the VdiOnSanNewIgroups object"""

    initiators = fields.List(fields.Str)
    r""" The initiators field of the vdi_on_san_new_igroups.
 """
    name = fields.Str()
    r""" The name of the new initiator group. Required in the POST body and optional in the PATCH body
 """
    protocol = fields.Str()
    r""" The protocol of the new initiator group. Optional in the POST or PATCH body

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return VdiOnSanNewIgroups

    @property
    def patchable_fields(self):
        return [
            "initiators",
            "name",
            "protocol",
        ]

    @property
    def postable_fields(self):
        return [
            "initiators",
            "name",
            "protocol",
        ]


class VdiOnSanNewIgroups(Resource):  # pylint: disable=missing-docstring

    _schema = VdiOnSanNewIgroupsSchema
