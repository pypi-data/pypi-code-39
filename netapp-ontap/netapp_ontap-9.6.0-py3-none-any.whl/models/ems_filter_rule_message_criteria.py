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


__all__ = ["EmsFilterRuleMessageCriteria", "EmsFilterRuleMessageCriteriaSchema"]
__pdoc__ = {
    "EmsFilterRuleMessageCriteriaSchema.resource": False,
    "EmsFilterRuleMessageCriteria": False,
}


class EmsFilterRuleMessageCriteriaSchema(ResourceSchema):
    """The fields of the EmsFilterRuleMessageCriteria object"""

    links = fields.Nested("RelatedLinkSchema", unknown=EXCLUDE)
    r""" The links field of the ems_filter_rule_message_criteria.
 """
    name_pattern = fields.Str()
    r""" Message name filter on which to match. Supports wildcards. Defaults to * if not specified.

Example: callhome.* """
    severities = fields.Str()
    r""" A comma-separated list of severities or a wildcard.

Example: error,informational """
    snmp_trap_types = fields.Str()
    r""" A comma separated list of snmp_trap_types or a wildcard.

Example: standard|built_in """

    @property
    def resource(self):
        return EmsFilterRuleMessageCriteria

    @property
    def patchable_fields(self):
        return [
            "name_pattern",
            "severities",
            "snmp_trap_types",
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name_pattern",
            "severities",
            "snmp_trap_types",
        ]


class EmsFilterRuleMessageCriteria(Resource):  # pylint: disable=missing-docstring

    _schema = EmsFilterRuleMessageCriteriaSchema
