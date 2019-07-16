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


__all__ = ["SnapmirrorPolicyRule", "SnapmirrorPolicyRuleSchema"]
__pdoc__ = {
    "SnapmirrorPolicyRuleSchema.resource": False,
    "SnapmirrorPolicyRule": False,
}


class SnapmirrorPolicyRuleSchema(ResourceSchema):
    """The fields of the SnapmirrorPolicyRule object"""

    count = fields.Integer()
    r""" Number of Snapshot copies to be kept for retention.

Example: 7 """
    creation_schedule = fields.Nested("ScheduleSchema", unknown=EXCLUDE)
    r""" The creation_schedule field of the snapmirror_policy_rule.
 """
    label = fields.Str()
    r""" Snapshot copy label

Example: hourly """
    prefix = fields.Str()
    r""" Specifies the prefix for the Snapshot copy name to be created as per the schedule. If no value is specified, then the label is used as the prefix.
 """

    @property
    def resource(self):
        return SnapmirrorPolicyRule

    @property
    def patchable_fields(self):
        return [
            "count",
            "label",
            "prefix",
        ]

    @property
    def postable_fields(self):
        return [
            "count",
            "creation_schedule",
            "label",
            "prefix",
        ]


class SnapmirrorPolicyRule(Resource):  # pylint: disable=missing-docstring

    _schema = SnapmirrorPolicyRuleSchema
