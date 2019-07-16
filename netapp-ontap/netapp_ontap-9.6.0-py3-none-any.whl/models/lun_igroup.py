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


__all__ = ["LunIgroup", "LunIgroupSchema"]
__pdoc__ = {
    "LunIgroupSchema.resource": False,
    "LunIgroup": False,
}


class LunIgroupSchema(ResourceSchema):
    """The fields of the LunIgroup object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the lun_igroup.
 """
    name = fields.Str()
    r""" The name of the initiator group.


Example: igroup1 """
    uuid = fields.Str()
    r""" The unique identifier of the initiator group.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunIgroup

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
        ]


class LunIgroup(Resource):  # pylint: disable=missing-docstring

    _schema = LunIgroupSchema
