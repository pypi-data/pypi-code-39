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


__all__ = ["SqlOnSanTempDb", "SqlOnSanTempDbSchema"]
__pdoc__ = {
    "SqlOnSanTempDbSchema.resource": False,
    "SqlOnSanTempDb": False,
}


class SqlOnSanTempDbSchema(ResourceSchema):
    """The fields of the SqlOnSanTempDb object"""

    size = fields.Integer()
    r""" The size of the temp db. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Optional in the POST or PATCH body
 """
    storage_service = fields.Nested("SqlOnSanTempDbStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the sql_on_san_temp_db.
 """

    @property
    def resource(self):
        return SqlOnSanTempDb

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


class SqlOnSanTempDb(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSanTempDbSchema
