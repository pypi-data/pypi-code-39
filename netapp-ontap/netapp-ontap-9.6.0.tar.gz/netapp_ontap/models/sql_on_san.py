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


__all__ = ["SqlOnSan", "SqlOnSanSchema"]
__pdoc__ = {
    "SqlOnSanSchema.resource": False,
    "SqlOnSan": False,
}


class SqlOnSanSchema(ResourceSchema):
    """The fields of the SqlOnSan object"""

    db = fields.Nested("SqlOnSanDbSchema", unknown=EXCLUDE)
    r""" The db field of the sql_on_san.
 """
    igroup_name = fields.Str()
    r""" The name of the initiator group through which the contents of this application will be accessed. Modification of this parameter is a disruptive operation. All LUNs in the application component will be unmapped from the current igroup and re-mapped to the new igroup. Required in the POST body and optional in the PATCH body
 """
    log = fields.Nested("SqlOnSanLogSchema", unknown=EXCLUDE)
    r""" The log field of the sql_on_san.
 """
    new_igroups = fields.Nested("SqlOnSanNewIgroupsSchema", unknown=EXCLUDE, many=True)
    r""" The list of initiator groups to create. Optional in the POST or PATCH body
 """
    os_type = fields.Str()
    r""" The name of the host OS running the application. Optional in the POST body

Valid choices:

* windows
* windows_2008
* windows_gpt """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the sql_on_san.
 """
    server_cores_count = fields.Integer()
    r""" The number of server cores for the db. Optional in the POST body
 """
    temp_db = fields.Nested("SqlOnSanTempDbSchema", unknown=EXCLUDE)
    r""" The temp_db field of the sql_on_san.
 """

    @property
    def resource(self):
        return SqlOnSan

    @property
    def patchable_fields(self):
        return [
            "igroup_name",
        ]

    @property
    def postable_fields(self):
        return [
            "db",
            "igroup_name",
            "log",
            "new_igroups",
            "os_type",
            "protection_type",
            "server_cores_count",
            "temp_db",
        ]


class SqlOnSan(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSanSchema
