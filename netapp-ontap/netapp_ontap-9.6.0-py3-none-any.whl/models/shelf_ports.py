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


__all__ = ["ShelfPorts", "ShelfPortsSchema"]
__pdoc__ = {
    "ShelfPortsSchema.resource": False,
    "ShelfPorts": False,
}


class ShelfPortsSchema(ResourceSchema):
    """The fields of the ShelfPorts object"""

    cable = fields.Nested("ShelfCableSchema", unknown=EXCLUDE)
    r""" The cable field of the shelf_ports.
 """
    designator = fields.Str()
    r""" The designator field of the shelf_ports.

Valid choices:

* circle
* square
* 1
* 2
* 3
* 4 """
    id = fields.Integer()
    r""" The id field of the shelf_ports.

Example: 0 """
    internal = fields.Boolean()
    r""" The internal field of the shelf_ports.
 """
    mac_address = fields.Str()
    r""" The mac_address field of the shelf_ports.
 """
    module_id = fields.Str()
    r""" The module_id field of the shelf_ports.

Valid choices:

* a
* b """
    remote = fields.Nested("ShelfRemoteSchema", unknown=EXCLUDE)
    r""" The remote field of the shelf_ports.
 """
    state = fields.Str()
    r""" The state field of the shelf_ports.

Valid choices:

* connected
* disconnected
* error """
    wwn = fields.Str()
    r""" The wwn field of the shelf_ports.

Example: 500A0980000B6C3F """

    @property
    def resource(self):
        return ShelfPorts

    @property
    def patchable_fields(self):
        return [
            "designator",
            "id",
            "internal",
            "mac_address",
            "module_id",
            "state",
            "wwn",
        ]

    @property
    def postable_fields(self):
        return [
            "cable",
            "designator",
            "id",
            "internal",
            "mac_address",
            "module_id",
            "remote",
            "state",
            "wwn",
        ]


class ShelfPorts(Resource):  # pylint: disable=missing-docstring

    _schema = ShelfPortsSchema
