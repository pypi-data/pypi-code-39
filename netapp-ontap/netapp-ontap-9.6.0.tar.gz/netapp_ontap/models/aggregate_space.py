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


__all__ = ["AggregateSpace", "AggregateSpaceSchema"]
__pdoc__ = {
    "AggregateSpaceSchema.resource": False,
    "AggregateSpace": False,
}


class AggregateSpaceSchema(ResourceSchema):
    """The fields of the AggregateSpace object"""

    block_storage = fields.Nested("AggregateSpaceBlockStorageSchema", unknown=EXCLUDE)
    r""" The block_storage field of the aggregate_space.
 """
    cloud_storage = fields.Nested("AggregateSpaceCloudStorageSchema", unknown=EXCLUDE)
    r""" The cloud_storage field of the aggregate_space.
 """
    efficiency = fields.Nested("SpaceEfficiencySchema", unknown=EXCLUDE)
    r""" The efficiency field of the aggregate_space.
 """
    efficiency_without_snapshots = fields.Nested("SpaceEfficiencySchema", unknown=EXCLUDE)
    r""" The efficiency_without_snapshots field of the aggregate_space.
 """
    footprint = fields.Integer()
    r""" A summation of volume footprints (including volume guarantees), in bytes. This includes all of the volume footprints in the block_storage tier and the cloud_storage tier.
This is an advanced property; there is an added cost to retrieving its value. The field is not populated for either a collection GET or an instance GET unless it is explicitly requested using the <i>fields</i> query parameter containing either footprint or **.


Example: 608896 """

    @property
    def resource(self):
        return AggregateSpace

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "block_storage",
            "cloud_storage",
            "efficiency",
            "efficiency_without_snapshots",
        ]


class AggregateSpace(Resource):  # pylint: disable=missing-docstring

    _schema = AggregateSpaceSchema
