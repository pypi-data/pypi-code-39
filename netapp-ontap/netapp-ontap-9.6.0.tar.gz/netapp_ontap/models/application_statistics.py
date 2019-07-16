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


__all__ = ["ApplicationStatistics", "ApplicationStatisticsSchema"]
__pdoc__ = {
    "ApplicationStatisticsSchema.resource": False,
    "ApplicationStatistics": False,
}


class ApplicationStatisticsSchema(ResourceSchema):
    """The fields of the ApplicationStatistics object"""

    components = fields.Nested("ApplicationStatisticsComponentsSchema", unknown=EXCLUDE, many=True)
    r""" The components field of the application_statistics.
 """
    iops = fields.Nested("ApplicationStatisticsIops1Schema", unknown=EXCLUDE)
    r""" The iops field of the application_statistics.
 """
    latency = fields.Nested("ApplicationStatisticsLatency1Schema", unknown=EXCLUDE)
    r""" The latency field of the application_statistics.
 """
    shared_storage_pool = fields.Boolean()
    r""" An application is considered to use a shared storage pool if storage elements for multiple components reside on the same aggregate
 """
    snapshot = fields.Nested("ApplicationStatisticsSnapshotSchema", unknown=EXCLUDE)
    r""" The snapshot field of the application_statistics.
 """
    space = fields.Nested("ApplicationStatisticsSpace1Schema", unknown=EXCLUDE)
    r""" The space field of the application_statistics.
 """
    statistics_incomplete = fields.Boolean()
    r""" If not all storage elements of the application are currently available, the returned statistics might only include data from those elements that were available
 """

    @property
    def resource(self):
        return ApplicationStatistics

    @property
    def patchable_fields(self):
        return [
        ]

    @property
    def postable_fields(self):
        return [
            "iops",
            "latency",
            "snapshot",
            "space",
        ]


class ApplicationStatistics(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationStatisticsSchema
