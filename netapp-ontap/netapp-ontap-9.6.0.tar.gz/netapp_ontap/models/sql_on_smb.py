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


__all__ = ["SqlOnSmb", "SqlOnSmbSchema"]
__pdoc__ = {
    "SqlOnSmbSchema.resource": False,
    "SqlOnSmb": False,
}


class SqlOnSmbSchema(ResourceSchema):
    """The fields of the SqlOnSmb object"""

    access = fields.Nested("SqlOnSmbAccessSchema", unknown=EXCLUDE)
    r""" The access field of the sql_on_smb.
 """
    db = fields.Nested("SqlOnSanDbSchema", unknown=EXCLUDE)
    r""" The db field of the sql_on_smb.
 """
    log = fields.Nested("SqlOnSanLogSchema", unknown=EXCLUDE)
    r""" The log field of the sql_on_smb.
 """
    protection_type = fields.Nested("MongoDbOnSanProtectionTypeSchema", unknown=EXCLUDE)
    r""" The protection_type field of the sql_on_smb.
 """
    server_cores_count = fields.Integer()
    r""" The number of server cores for the db. Optional in the POST body
 """
    temp_db = fields.Nested("SqlOnSanTempDbSchema", unknown=EXCLUDE)
    r""" The temp_db field of the sql_on_smb.
 """

    @property
    def resource(self):
        return SqlOnSmb

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "access",
            "db",
            "log",
            "protection_type",
            "server_cores_count",
            "temp_db",
        ]


class SqlOnSmb(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSmbSchema
