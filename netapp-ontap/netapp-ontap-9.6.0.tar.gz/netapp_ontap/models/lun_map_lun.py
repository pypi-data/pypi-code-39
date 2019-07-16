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


__all__ = ["LunMapLun", "LunMapLunSchema"]
__pdoc__ = {
    "LunMapLunSchema.resource": False,
    "LunMapLun": False,
}


class LunMapLunSchema(ResourceSchema):
    """The fields of the LunMapLun object"""

    links = fields.Nested("SelfLinkSchema", unknown=EXCLUDE)
    r""" The links field of the lun_map_lun.
 """
    name = fields.Str()
    r""" The fully qualified path name of the LUN composed of a \"/vol\" prefix, the volume name, the (optional) qtree name, and file name of the LUN. Valid in POST.


Example: /vol/volume1/qtree1/lun1 """
    node = fields.Nested("LunMapLunNodeSchema", unknown=EXCLUDE)
    r""" The node field of the lun_map_lun.
 """
    uuid = fields.Str()
    r""" The unique identifier of the LUN. Valid in POST.


Example: 1cd8a442-86d1-11e0-ae1c-123478563412 """

    @property
    def resource(self):
        return LunMapLun

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "links",
            "name",
            "node",
            "uuid",
        ]


class LunMapLun(Resource):  # pylint: disable=missing-docstring

    _schema = LunMapLunSchema
