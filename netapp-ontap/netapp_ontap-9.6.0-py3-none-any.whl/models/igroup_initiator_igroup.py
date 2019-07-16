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


__all__ = ["IgroupInitiatorIgroup", "IgroupInitiatorIgroupSchema"]
__pdoc__ = {
    "IgroupInitiatorIgroupSchema.resource": False,
    "IgroupInitiatorIgroup": False,
}


class IgroupInitiatorIgroupSchema(ResourceSchema):
    """The fields of the IgroupInitiatorIgroup object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the igroup_initiator_igroup.
 """
    uuid = fields.Str()
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupInitiatorIgroup

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class IgroupInitiatorIgroup(Resource):  # pylint: disable=missing-docstring

    _schema = IgroupInitiatorIgroupSchema
