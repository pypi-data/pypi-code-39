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


__all__ = ["AggregateBlockStorageHybridCache", "AggregateBlockStorageHybridCacheSchema"]
__pdoc__ = {
    "AggregateBlockStorageHybridCacheSchema.resource": False,
    "AggregateBlockStorageHybridCache": False,
}


class AggregateBlockStorageHybridCacheSchema(ResourceSchema):
    """The fields of the AggregateBlockStorageHybridCache object"""

    disk_count = fields.Integer()
    r""" Number of disks used in the cache tier of the aggregate. Only provided when hybrid_cache.enabled is 'true'.

Example: 6 """
    enabled = fields.Boolean()
    r""" Aggregate uses HDDs with SSDs as a cache
 """
    raid_type = fields.Str()
    r""" RAID type for SSD cache of the aggregate. Only provided when hybrid_cache.enabled is 'true'.

Valid choices:

* raid_dp
* raid_tec
* raid4 """
    size = fields.Integer()
    r""" Total usable space in bytes of SSD cache. Only provided when hybrid_cache.enabled is 'true'.

Example: 1612709888 """
    used = fields.Integer()
    r""" Space used in bytes of SSD cache. Only provided when hybrid_cache.enabled is 'true'.

Example: 26501122 """

    @property
    def resource(self):
        return AggregateBlockStorageHybridCache

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
        ]


class AggregateBlockStorageHybridCache(Resource):  # pylint: disable=missing-docstring

    _schema = AggregateBlockStorageHybridCacheSchema
