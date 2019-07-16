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


__all__ = ["IgroupLun", "IgroupLunSchema"]
__pdoc__ = {
    "IgroupLunSchema.resource": False,
    "IgroupLun": False,
}


class IgroupLunSchema(ResourceSchema):
    """The fields of the IgroupLun object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the igroup_lun.
 """
    name = fields.Str()
    r""" The name of the LUN.


Example: lun1 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the igroup_lun.
 """
    uuid = fields.Str()
    r""" The unique identifier of the LUN.


Example: 4ea7a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return IgroupLun

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "node",
        ]


class IgroupLun(Resource):  # pylint: disable=missing-docstring

    _schema = IgroupLunSchema
