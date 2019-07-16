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


__all__ = ["NodeHa", "NodeHaSchema"]
__pdoc__ = {
    "NodeHaSchema.resource": False,
    "NodeHa": False,
}


class NodeHaSchema(ResourceSchema):
    """The fields of the NodeHa object"""

    auto_giveback = fields.Boolean()
    r""" Specifies whether giveback is automatically initiated when the node that owns the storage is ready.
 """
    enabled = fields.Boolean()
    r""" Specifies whether or not storage failover is enabled.
 """
    partners = fields.Nested("NodeSchema", unknown=EXCLUDE, many=True)
    r""" The nodes in this node's High Availability (HA) group.
 """

    @property
    def resource(self):
        return NodeHa

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class NodeHa(Resource):  # pylint: disable=missing-docstring

    _schema = NodeHaSchema
