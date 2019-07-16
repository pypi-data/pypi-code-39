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


__all__ = ["QuotaRuleGroup", "QuotaRuleGroupSchema"]
__pdoc__ = {
    "QuotaRuleGroupSchema.resource": False,
    "QuotaRuleGroup": False,
}


class QuotaRuleGroupSchema(ResourceSchema):
    """The fields of the QuotaRuleGroup object"""

    id = fields.Str()
    r""" Quota target group ID
 """
    name = fields.Str()
    r""" Quota target group name
 """

    @property
    def resource(self):
        return QuotaRuleGroup

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class QuotaRuleGroup(Resource):  # pylint: disable=missing-docstring

    _schema = QuotaRuleGroupSchema
