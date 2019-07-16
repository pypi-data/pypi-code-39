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


__all__ = ["SqlOnSmbAccess", "SqlOnSmbAccessSchema"]
__pdoc__ = {
    "SqlOnSmbAccessSchema.resource": False,
    "SqlOnSmbAccess": False,
}


class SqlOnSmbAccessSchema(ResourceSchema):
    """The fields of the SqlOnSmbAccess object"""

    installer = fields.Str()
    r""" SQL installer admin user name. Optional in the POST body
 """
    service_account = fields.Str()
    r""" SQL service account user name. Required in the POST body
 """

    @property
    def resource(self):
        return SqlOnSmbAccess

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "installer",
            "service_account",
        ]


class SqlOnSmbAccess(Resource):  # pylint: disable=missing-docstring

    _schema = SqlOnSmbAccessSchema
