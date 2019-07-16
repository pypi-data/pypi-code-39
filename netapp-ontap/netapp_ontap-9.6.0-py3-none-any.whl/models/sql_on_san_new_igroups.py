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


__all__ = ["SqlOnSanNewIgroups", "SqlOnSanNewIgroupsSchema"]
__pdoc__ = {
    "SqlOnSanNewIgroupsSchema.resource": False,
    "SqlOnSanNewIgroups": False,
}


class SqlOnSanNewIgroupsSchema(ResourceSchema):
    """The fields of the SqlOnSanNewIgroups object"""

    initiators = fields.List(fields.Str)
    r""" The initiators field of the sql_on_san_new_igroups.
 """
    name = fields.Str()
    r""" The name of the new initiator group. Required in the POST body and optional in the PATCH body
 """
    os_type = fields.Str()
    r""" The name of the host OS accessing the application. The default value is the host OS that is running the application. Optional in the POST or PATCH body

Valid choices:

* hyper_v
* vmware
* windows """
    protocol = fields.Str()
    r""" The protocol of the new initiator group. Optional in the POST or PATCH body

Valid choices:

* fcp
* iscsi
* mixed """

    @property
    def resource(self):
        return SqlOnSanNewIgroups

    @property
    def patchable_fields(self):
        return [
            "initiators",
            "name",
            "os_type",
            "protocol",
        ]

    @property
    def postable_fields(self):
        return [
            "initiators",
            "name",
            "os_type",
            "protocol",
        ]


class SqlOnSanNewIgroups(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSanNewIgroupsSchema
