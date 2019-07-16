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


__all__ = ["AutosupportIssues", "AutosupportIssuesSchema"]
__pdoc__ = {
    "AutosupportIssuesSchema.resource": False,
    "AutosupportIssues": False,
}


class AutosupportIssuesSchema(ResourceSchema):
    """The fields of the AutosupportIssues object"""

    corrective_action = fields.Nested("AutosupportConnectivityCorrectiveActionSchema", unknown=EXCLUDE)
    r""" The corrective_action field of the autosupport_issues.
 """
    issue = fields.Nested("AutosupportConnectivityIssueSchema", unknown=EXCLUDE)
    r""" The issue field of the autosupport_issues.
 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the autosupport_issues.
 """

    @property
    def resource(self):
        return AutosupportIssues

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "corrective_action",
            "issue",
            "node",
        ]


class AutosupportIssues(Resource):  # pylint: disable=missing-docstring

    _schema = AutosupportIssuesSchema
