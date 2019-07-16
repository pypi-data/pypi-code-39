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


__all__ = ["ApplicationStatisticsComponents", "ApplicationStatisticsComponentsSchema"]
__pdoc__ = {
    "ApplicationStatisticsComponentsSchema.resource": False,
    "ApplicationStatisticsComponents": False,
}


class ApplicationStatisticsComponentsSchema(ResourceSchema):
    """The fields of the ApplicationStatisticsComponents object"""

    iops = fields.Nested("ApplicationStatisticsIopsSchema", unknown=EXCLUDE)
    r""" The iops field of the application_statistics_components.
 """
    latency = fields.Nested("ApplicationStatisticsLatencySchema", unknown=EXCLUDE)
    r""" The latency field of the application_statistics_components.
 """
    name = fields.Str()
    r""" Component Name
 """
    shared_storage_pool = fields.Boolean()
    r""" An application component is considered to use a shared storage pool if storage elements for for other components reside on the same aggregate as storage elements for this component
 """
    snapshot = fields.Nested("ApplicationStatisticsSnapshotSchema", unknown=EXCLUDE)
    r""" The snapshot field of the application_statistics_components.
 """
    space = fields.Nested("ApplicationStatisticsSpaceSchema", unknown=EXCLUDE)
    r""" The space field of the application_statistics_components.
 """
    statistics_incomplete = fields.Boolean()
    r""" If not all storage elements of the application component are currently available, the returned statistics might only include data from those elements that were available
 """
    storage_service = fields.Nested("ApplicationStatisticsStorageServiceSchema", unknown=EXCLUDE)
    r""" The storage_service field of the application_statistics_components.
 """
    uuid = fields.Str()
    r""" Component UUID
 """

    @property
    def resource(self):
        return ApplicationStatisticsComponents

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
            "storage_service",
        ]


class ApplicationStatisticsComponents(Resource):  # pylint: disable=missing-docstring

    _schema = ApplicationStatisticsComponentsSchema
