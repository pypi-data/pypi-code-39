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


__all__ = ["IgroupLunMaps", "IgroupLunMapsSchema"]
__pdoc__ = {
    "IgroupLunMapsSchema.resource": False,
    "IgroupLunMaps": False,
}


class IgroupLunMapsSchema(ResourceSchema):
    """The fields of the IgroupLunMaps object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the igroup_lun_maps.
 """
    logical_unit_number = fields.Integer()
    r""" The logical unit number assigned to the LUN for initiators in the initiator group.
 """
    lun = fields.Nested("IgroupLunSchema", unknown=EXCLUDE)
    r""" The lun field of the igroup_lun_maps.
 """

    @property
    def resource(self):
        return IgroupLunMaps

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "lun",
        ]


class IgroupLunMaps(Resource):  # pylint: disable=missing-docstring

    _schema = IgroupLunMapsSchema
