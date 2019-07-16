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


__all__ = ["NodeControllerFlashCache", "NodeControllerFlashCacheSchema"]
__pdoc__ = {
    "NodeControllerFlashCacheSchema.resource": False,
    "NodeControllerFlashCache": False,
}


class NodeControllerFlashCacheSchema(ResourceSchema):
    """The fields of the NodeControllerFlashCache object"""

    capacity = fields.Integer()
    r""" Size in bytes

Example: 1024000000000 """
    firmware_version = fields.Str()
    r""" The firmware_version field of the node_controller_flash_cache.

Example: NA05 """
    hardware_revision = fields.Str()
    r""" The hardware_revision field of the node_controller_flash_cache.

Example: A1 """
    model = fields.Str()
    r""" The model field of the node_controller_flash_cache.

Example: X1970A """
    part_number = fields.Str()
    r""" The part_number field of the node_controller_flash_cache.

Example: 119-00207 """
    serial_number = fields.Str()
    r""" The serial_number field of the node_controller_flash_cache.

Example: A22P5061550000187 """
    slot = fields.Str()
    r""" The slot field of the node_controller_flash_cache.

Example: 6-1 """
    state = fields.Str()
    r""" The state field of the node_controller_flash_cache.

Valid choices:

* ok
* erasing
* erased
* failed
* removed """

    @property
    def resource(self):
        return NodeControllerFlashCache

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class NodeControllerFlashCache(Resource):  # pylint: disable=missing-docstring

    _schema = NodeControllerFlashCacheSchema
