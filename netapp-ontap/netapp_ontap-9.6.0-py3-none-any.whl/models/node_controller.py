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


__all__ = ["NodeController", "NodeControllerSchema"]
__pdoc__ = {
    "NodeControllerSchema.resource": False,
    "NodeController": False,
}


class NodeControllerSchema(ResourceSchema):
    """The fields of the NodeController object"""

    flash_cache = fields.Nested("NodeControllerFlashCacheSchema", unknown=EXCLUDE, many=True)
    r""" A list of Flash-Cache devices. Only returned when requested by name.
 """
    frus = fields.Nested("NodeControllerFrusSchema", unknown=EXCLUDE, many=True)
    r""" A list of frus in the node. Only returned when requested by name.
 """
    over_temperature = fields.Str()
    r""" Specifies whether the hardware is currently operating outside of its recommended temperature range. The hardware shuts down if the temperature exceeds critical thresholds.

Valid choices:

* over
* normal """

    @property
    def resource(self):
        return NodeController

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "frus",
        ]


class NodeController(Resource):  # pylint: disable=missing-docstring

    _schema = NodeControllerSchema
