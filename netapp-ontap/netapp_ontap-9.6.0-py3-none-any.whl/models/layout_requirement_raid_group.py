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


__all__ = ["LayoutRequirementRaidGroup", "LayoutRequirementRaidGroupSchema"]
__pdoc__ = {
    "LayoutRequirementRaidGroupSchema.resource": False,
    "LayoutRequirementRaidGroup": False,
}


class LayoutRequirementRaidGroupSchema(ResourceSchema):
    """The fields of the LayoutRequirementRaidGroup object"""

    default = fields.Integer()
    r""" Default number of disks in a RAID group

Example: 16 """
    max = fields.Integer()
    r""" Maximum number of disks allowed in a RAID group

Example: 28 """
    min = fields.Integer()
    r""" Minimum number of disks allowed in a RAID group

Example: 5 """

    @property
    def resource(self):
        return LayoutRequirementRaidGroup

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class LayoutRequirementRaidGroup(Resource):  # pylint: disable=missing-docstring

    _schema = LayoutRequirementRaidGroupSchema
