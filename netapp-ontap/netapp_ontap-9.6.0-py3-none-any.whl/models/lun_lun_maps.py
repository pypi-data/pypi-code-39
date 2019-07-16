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


__all__ = ["LunLunMaps", "LunLunMapsSchema"]
__pdoc__ = {
    "LunLunMapsSchema.resource": False,
    "LunLunMaps": False,
}


class LunLunMapsSchema(ResourceSchema):
    """The fields of the LunLunMaps object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the lun_lun_maps.
 """
    igroup = fields.Nested("LunIgroupSchema", unknown=EXCLUDE)
    r""" The igroup field of the lun_lun_maps.
 """
    logical_unit_number = fields.Integer()
    r""" The logical unit number assigned to the LUN for initiators in the initiator group.
 """

    @property
    def resource(self):
        return LunLunMaps

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "igroup",
        ]


class LunLunMaps(Resource):  # pylint: disable=missing-docstring

    _schema = LunLunMapsSchema
