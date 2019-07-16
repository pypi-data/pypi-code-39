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


__all__ = ["QuotaRuleQtree", "QuotaRuleQtreeSchema"]
__pdoc__ = {
    "QuotaRuleQtreeSchema.resource": False,
    "QuotaRuleQtree": False,
}


class QuotaRuleQtreeSchema(ResourceSchema):
    """The fields of the QuotaRuleQtree object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the quota_rule_qtree.
 """
    id = fields.Integer()
    r""" The unique identifier for a qtree.

Example: 1 """
    name = fields.Str()
    r""" The name of the qtree.

Example: qt1 """

    @property
    def resource(self):
        return QuotaRuleQtree

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


class QuotaRuleQtree(Resource):  # pylint: disable=missing-docstring

    _schema = QuotaRuleQtreeSchema
