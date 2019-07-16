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


__all__ = ["QuotaReportUsers", "QuotaReportUsersSchema"]
__pdoc__ = {
    "QuotaReportUsersSchema.resource": False,
    "QuotaReportUsers": False,
}


class QuotaReportUsersSchema(ResourceSchema):
    """The fields of the QuotaReportUsers object"""

    id = fields.Str()
    r""" Quota target user ID
 """
    name = fields.Str()
    r""" Quota target user name
 """

    @property
    def resource(self):
        return QuotaReportUsers

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class QuotaReportUsers(Resource):  # pylint: disable=missing-docstring

    _schema = QuotaReportUsersSchema
