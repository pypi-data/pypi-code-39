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


__all__ = ["QuotaReportFiles", "QuotaReportFilesSchema"]
__pdoc__ = {
    "QuotaReportFilesSchema.resource": False,
    "QuotaReportFiles": False,
}


class QuotaReportFilesSchema(ResourceSchema):
    """The fields of the QuotaReportFiles object"""

    hard_limit = fields.Integer()
    r""" File hard limit
 """
    soft_limit = fields.Integer()
    r""" File soft limit
 """
    used = fields.Nested("QuotaReportFilesUsedSchema", unknown=EXCLUDE)
    r""" The used field of the quota_report_files.
 """

    @property
    def resource(self):
        return QuotaReportFiles

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "used",
        ]


class QuotaReportFiles(Resource):  # pylint: disable=missing-docstring

    _schema = QuotaReportFilesSchema
