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


__all__ = ["OracleOnNfsDb", "OracleOnNfsDbSchema"]
__pdoc__ = {
    "OracleOnNfsDbSchema.resource": False,
    "OracleOnNfsDb": False,
}


class OracleOnNfsDbSchema(ResourceSchema):
    """The fields of the OracleOnNfsDb object"""

    size = fields.Integer()
    r""" The size of the database. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body and optional in the PATCH body
 """
    storage_service = fields.Nested("MongoDbOnSanDatasetStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the oracle_on_nfs_db.
 """

    @property
    def resource(self):
        return OracleOnNfsDb

    @property
    def patchable_fields(self):
        return [
            "size",
        ]

    @property
    def postable_fields(self):
        return [
            "size",
            "storage_service",
        ]


class OracleOnNfsDb(Resource):  # pylint: disable=missing-docstring

    _schema = OracleOnNfsDbSchema
