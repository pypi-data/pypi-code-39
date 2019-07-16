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


__all__ = ["QuotaReportQtree", "QuotaReportQtreeSchema"]
__pdoc__ = {
    "QuotaReportQtreeSchema.resource": False,
    "QuotaReportQtree": False,
}


class QuotaReportQtreeSchema(ResourceSchema):
    """The fields of the QuotaReportQtree object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the quota_report_qtree.
 """
    id = fields.Integer()
    r""" The unique identifier for a qtree.

Example: 1 """
    name = fields.Str()
    r""" The name of the qtree.

Example: qt1 """

    @property
    def resource(self):
        return QuotaReportQtree

    @property
    def patchable_fields(self):
        return [
            "id",
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "id",
            "name",
        ]


class QuotaReportQtree(Resource):  # pylint: disable=missing-docstring

    _schema = QuotaReportQtreeSchema
