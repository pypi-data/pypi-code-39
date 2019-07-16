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


__all__ = ["PerformanceMetricIoType", "PerformanceMetricIoTypeSchema"]
__pdoc__ = {
    "PerformanceMetricIoTypeSchema.resource": False,
    "PerformanceMetricIoType": False,
}


class PerformanceMetricIoTypeSchema(ResourceSchema):
    """The fields of the PerformanceMetricIoType object"""

    other = fields.Integer()
    r""" Performance metric for other I/O operations. Other I/O operations can be metadata operations, such as directory lookups and so on.
 """
    read = fields.Integer()
    r""" Performance metric for read I/O operations.

Example: 200 """
    total = fields.Integer()
    r""" Performance metric aggregated over all types of I/O operations.

Example: 1000 """
    write = fields.Integer()
    r""" Peformance metric for write I/O operations.

Example: 100 """

    @property
    def resource(self):
        return PerformanceMetricIoType

    @property
    def patchable_fields(self):
        return [
            "other",
            "read",
            "total",
            "write",
        ]

    @property
    def postable_fields(self):
        return [
            "other",
            "read",
            "total",
            "write",
        ]


class PerformanceMetricIoType(Resource):  # pylint: disable=missing-docstring

    _schema = PerformanceMetricIoTypeSchema
