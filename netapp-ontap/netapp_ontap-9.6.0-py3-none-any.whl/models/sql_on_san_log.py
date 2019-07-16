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


__all__ = ["SqlOnSanLog", "SqlOnSanLogSchema"]
__pdoc__ = {
    "SqlOnSanLogSchema.resource": False,
    "SqlOnSanLog": False,
}


class SqlOnSanLogSchema(ResourceSchema):
    """The fields of the SqlOnSanLog object"""

    size = fields.Integer()
    r""" The size of the log db. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body and optional in the PATCH body
 """
    storage_service = fields.Nested("SqlOnSanLogStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the sql_on_san_log.
 """

    @property
    def resource(self):
        return SqlOnSanLog

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


class SqlOnSanLog(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSanLogSchema
