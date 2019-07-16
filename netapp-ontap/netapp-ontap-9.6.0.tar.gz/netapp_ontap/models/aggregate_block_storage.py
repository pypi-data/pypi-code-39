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


__all__ = ["AggregateBlockStorage", "AggregateBlockStorageSchema"]
__pdoc__ = {
    "AggregateBlockStorageSchema.resource": False,
    "AggregateBlockStorage": False,
}


class AggregateBlockStorageSchema(ResourceSchema):
    """The fields of the AggregateBlockStorage object"""

    hybrid_cache = fields.Nested("AggregateBlockStorageHybridCacheSchema", unknown=EXCLUDE)
    r""" The hybrid_cache field of the aggregate_block_storage.
 """
    mirror = fields.Nested("AggregateBlockStorageMirrorSchema", unknown=EXCLUDE)
    r""" The mirror field of the aggregate_block_storage.
 """
    plexes = fields.Nested("PlexSchema", unknown=EXCLUDE, many=True)
    r""" Plex reference for each plex in the aggregate.
 """
    primary = fields.Nested("AggregateBlockStoragePrimarySchema", unknown=EXCLUDE)
    r""" The primary field of the aggregate_block_storage.
 """

    @property
    def resource(self):
        return AggregateBlockStorage

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "hybrid_cache",
            "mirror",
            "primary",
        ]


class AggregateBlockStorage(Resource):  # pylint: disable=missing-docstring

    _schema = AggregateBlockStorageSchema
