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


__all__ = ["VdiOnNasDesktops", "VdiOnNasDesktopsSchema"]
__pdoc__ = {
    "VdiOnNasDesktopsSchema.resource": False,
    "VdiOnNasDesktops": False,
}


class VdiOnNasDesktopsSchema(ResourceSchema):
    """The fields of the VdiOnNasDesktops object"""

    count = fields.Integer()
    r""" The number of desktops to support. Optional in the POST or PATCH body
 """
    size = fields.Integer()
    r""" The size of the desktops. Usage: {&lt;integer&gt;[KB|MB|GB|TB|PB]} Required in the POST body
 """
    storage_service = fields.Nested("VdiOnNasDesktopsStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the vdi_on_nas_desktops.
 """

    @property
    def resource(self):
        return VdiOnNasDesktops

    @property
    def patchable_fields(self):
        return [
            "count",
        ]

    @property
    def postable_fields(self):
        return [
            "count",
            "size",
            "storage_service",
        ]


class VdiOnNasDesktops(Resource):  # pylint: disable=missing-docstring

    _schema = VdiOnNasDesktopsSchema
