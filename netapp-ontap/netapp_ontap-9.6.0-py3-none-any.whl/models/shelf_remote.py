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


__all__ = ["ShelfRemote", "ShelfRemoteSchema"]
__pdoc__ = {
    "ShelfRemoteSchema.resource": False,
    "ShelfRemote": False,
}


class ShelfRemoteSchema(ResourceSchema):
    """The fields of the ShelfRemote object"""

    chassis = fields.Str()
    r""" The chassis field of the shelf_remote.
 """
    mac_address = fields.Str()
    r""" The mac_address field of the shelf_remote.
 """
    phy = fields.Str()
    r""" The phy field of the shelf_remote.

Example: 12 """
    port = fields.Str()
    r""" The port field of the shelf_remote.
 """
    wwn = fields.Str()
    r""" The wwn field of the shelf_remote.

Example: 50000D1703544B80 """

    @property
    def resource(self):
        return ShelfRemote

    @property
    def patchable_fields(self):
        return [
            "chassis",
            "mac_address",
            "phy",
            "port",
            "wwn",
        ]

    @property
    def postable_fields(self):
        return [
            "chassis",
            "mac_address",
            "phy",
            "port",
            "wwn",
        ]


class ShelfRemote(Resource):  # pylint: disable=missing-docstring

    _schema = ShelfRemoteSchema
