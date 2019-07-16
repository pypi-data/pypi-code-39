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


__all__ = ["SnapshotPolicySchedule", "SnapshotPolicyScheduleSchema"]
__pdoc__ = {
    "SnapshotPolicyScheduleSchema.resource": False,
    "SnapshotPolicySchedule": False,
}


class SnapshotPolicyScheduleSchema(ResourceSchema):
    """The fields of the SnapshotPolicySchedule object"""

    name = fields.Str()
    r""" Schedule at which Snapshot copies are captured on the volume. Some common schedules already defined in the system are hourly, daily, weekly, at 15 minute intervals, and at 5 minute intervals. Snapshot copy policies with custom schedules can be referenced.

Example: hourly """

    @property
    def resource(self):
        return SnapshotPolicySchedule

    @property
    def patchable_fields(self):
        return [
            "name",
        ]

    @property
    def postable_fields(self):
        return [
            "name",
        ]


class SnapshotPolicySchedule(Resource):  # pylint: disable=missing-docstring

    _schema = SnapshotPolicyScheduleSchema
