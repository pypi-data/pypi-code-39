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


__all__ = ["AggregateCloudStorage", "AggregateCloudStorageSchema"]
__pdoc__ = {
    "AggregateCloudStorageSchema.resource": False,
    "AggregateCloudStorage": False,
}


class AggregateCloudStorageSchema(ResourceSchema):
    """The fields of the AggregateCloudStorage object"""

    attach_eligible = fields.Boolean()
    r""" Aggregate is eligible for a cloud store to be attached.
 """
    stores = fields.Nested("CloudStorageTierSchema", unknown=EXCLUDE, many=True)
    r""" Configuration information for each cloud storage portion of the aggregate.
 """
    tiering_fullness_threshold = fields.Integer()
    r""" The percentage of space in the performance tier that must be used before data is tiered out to the cloud store. Only valid for PATCH operations.
 """

    @property
    def resource(self):
        return AggregateCloudStorage

    @property
    def patchable_fields(self):
        return [
            "tiering_fullness_threshold",
        ]

    @property
    def postable_fields(self):
        return [
            "tiering_fullness_threshold",
        ]


class AggregateCloudStorage(Resource):  # pylint: disable=missing-docstring

    _schema = AggregateCloudStorageSchema
