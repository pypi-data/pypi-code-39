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


__all__ = ["AggregateSpare", "AggregateSpareSchema"]
__pdoc__ = {
    "AggregateSpareSchema.resource": False,
    "AggregateSpare": False,
}


class AggregateSpareSchema(ResourceSchema):
    """The fields of the AggregateSpare object"""

    checksum_style = fields.Str()
    r""" The checksum type that has been assigned to the spares

Valid choices:

* block
* advanced_zoned """
    disk_class = fields.Str()
    r""" Disk class of spares

Valid choices:

* unknown
* capacity
* performance
* archive
* solid_state
* array
* virtual
* data_center
* capacity_flash """
    layout_requirements = fields.Nested("LayoutRequirementSchema", unknown=EXCLUDE, many=True)
    r""" Available RAID protections and their restrictions
 """
    node = fields.Nested("NodeSchema", unknown=EXCLUDE)
    r""" The node field of the aggregate_spare.
 """
    size = fields.Integer()
    r""" Usable size of each spare in bytes

Example: 10156769280 """
    syncmirror_pool = fields.Str()
    r""" SyncMirror spare pool

Valid choices:

* pool0
* pool1 """
    usable = fields.Integer()
    r""" Total number of usable spares

Example: 9 """

    @property
    def resource(self):
        return AggregateSpare

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "layout_requirements",
            "node",
        ]


class AggregateSpare(Resource):  # pylint: disable=missing-docstring

    _schema = AggregateSpareSchema
