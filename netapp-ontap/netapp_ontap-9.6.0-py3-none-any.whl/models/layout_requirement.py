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


__all__ = ["LayoutRequirement", "LayoutRequirementSchema"]
__pdoc__ = {
    "LayoutRequirementSchema.resource": False,
    "LayoutRequirement": False,
}


class LayoutRequirementSchema(ResourceSchema):
    """The fields of the LayoutRequirement object"""

    aggregate_min_disks = fields.Integer()
    r""" Minimum number of disks to create an aggregate

Example: 6 """
    default = fields.Boolean()
    r""" Indicates if this RAID type is the default
 """
    raid_group = fields.Nested("LayoutRequirementRaidGroupSchema", unknown=EXCLUDE)
    r""" The raid_group field of the layout_requirement.
 """
    raid_type = fields.Str()
    r""" RAID type

Valid choices:

* raid_dp
* raid_tec
* raid4
* raid0 """

    @property
    def resource(self):
        return LayoutRequirement

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "raid_group",
        ]


class LayoutRequirement(Resource):  # pylint: disable=missing-docstring

    _schema = LayoutRequirementSchema
